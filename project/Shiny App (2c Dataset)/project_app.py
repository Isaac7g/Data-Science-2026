# -------- Set Up --------------------------------------------------
from shiny import ui, render, App
import pandas as pd
import plotly.express as px
import re
import unicodedata

df = pd.read_csv("Combined_Data.csv", encoding="utf-8-sig")

# Clean and Tidy ---------------------------------------------------
def norm(x):
    x = unicodedata.normalize("NFKD", str(x)).replace("\u00a0", " ")
    return re.sub(r"[^a-z0-9]", "", x.lower())


def col(name):
    target = norm(name)
    matches = [c for c in df.columns if norm(c) == target]

    if not matches:
        matches = [c for c in df.columns if target in norm(c)]

    if not matches:
        raise KeyError(f"Column not found: {name}")

    return matches[0]


USE = col("How often do you use AI chatbots (e.g. Claude, ChatGPT, Gemini)?")

FAM = col(
    "Overall, how familiar are you with how AI systems work technically?"
)

FRAME = col(
    "When you use AI, which of the following best describes "
    "how you like to think of it?"
)

LIKERT = [
    col("I speak with AI"),
    col("AI sometimes gets confused"),
    col("AI intends to complete an action correctly"),
    col("Sometimes AI makes its own decisions"),
    col("AI understands what I say"),
    col("AI sometimes expresses excitement in its responses"),
    col("My intentions are sometimes anticipated by AI"),
    col("AI always aims to be as honest as it can be"),
]

ORDER = [
    "Strongly Disagree",
    "Disagree",
    "Somewhat Disagree",
    "Somewhat Agree",
    "Agree",
    "Strongly Agree",
]

LIKERT_SCORE = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Somewhat Disagree": 3,
    "Somewhat Agree": 4,
    "Agree": 5,
    "Strongly Agree": 6,
}

USE_ORDER = [
    "Never/rarely",
    "A few times a month",
    "About once a week",
    "Several times a week",
    "Daily",
]

FAM_ORDER = [
    "Not familiar (I can use them but don't know how they work)",
    "Somewhat familiar (I have a basic idea)",
    "Fairly familiar (I have a working understanding)",
    "Very familiar (I have a detailed, technical understanding)",
]

for c in [USE, FAM, FRAME] + LIKERT:
    df[c] = df[c].fillna("Not reported").astype(str).str.strip()


#---------- UI ---------------------------------------------------

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider(
            "age",
            "Age range",
            int(df.Age.min()),
            int(df.Age.max()),
            [int(df.Age.min()), int(df.Age.max())],
        ),

        ui.input_select(
            "use",
            "AI chatbot use",
            ["All"] + USE_ORDER
        ),

        ui.input_select(
            "fam",
            "Technical familiarity",
            ["All"] + FAM_ORDER
        ),
    ),

    ui.page_fluid(
        ui.h1("AI Use and Perceived Personhood"),

        ui.layout_columns(
            ui.value_box("Respondents", ui.output_text("n")),
            ui.value_box("Mean age", ui.output_text("mean_age")),
            ui.value_box("Personhood score", ui.output_text("personhood")),
        ),

        ui.output_ui("use_card"),

        ui.output_ui("fam_card"),

        ui.card(
            ui.card_header("Preferred framing of AI"),
            ui.output_ui("frame_chart")
        ),

        ui.card(
            ui.card_header("Attitudes towards AI"),
            ui.output_ui("likert_chart")
        ),
    ),
)


def data(input):
    d = df.copy()

    if input.use() != "All":
        d = d[d[USE] == input.use()]

    if input.fam() != "All":
        d = d[d[FAM] == input.fam()]

    return d[
        (d.Age >= input.age()[0]) &
        (d.Age <= input.age()[1])
    ]


def bar(series):

    counts = series.value_counts().reset_index()
    counts.columns = ["Response", "Count"]

    responses = set(counts["Response"])

    if responses.issubset(set(USE_ORDER)):
        counts["Response"] = pd.Categorical(
            counts["Response"],
            categories=USE_ORDER,
            ordered=True,
        )
        counts = counts.sort_values("Response")

    elif responses.issubset(set(FAM_ORDER)):
        counts["Response"] = pd.Categorical(
            counts["Response"],
            categories=FAM_ORDER,
            ordered=True,
        )
        counts = counts.sort_values("Response")

    fig = px.bar(
        counts,
        x="Count",
        y="Response",
        orientation="h",
        text="Count"
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        showlegend=False
    )

    return ui.HTML(
        fig.to_html(
            full_html=False,
            include_plotlyjs="cdn"
        )
    )

# -------------- SERVER -----------------------------------------------------

def server(input, output, session):

    @render.text
    def n():
        return f"{len(data(input)):,}"

    @render.text
    def mean_age():
        return f"{data(input).Age.mean():.1f}"

    @render.text
    def personhood():

        d = data(input)

        scores = (
            d[LIKERT]
            .replace(LIKERT_SCORE)
            .apply(pd.to_numeric, errors="coerce"))

        mean_score = scores.stack().mean()

        if pd.isna(mean_score):
            return "N/A"

        # Rescale the 1-6 average onto 0-100%
        percentage = (mean_score - 1) / 5 * 100

        return f"{percentage:.1f}%"

    @render.ui
    def use_card():

        if input.use() != "All":
            return None

        return ui.card(
            ui.card_header("AI chatbot use"),
            bar(data(input)[USE])
        )

    @render.ui
    def fam_card():

        if input.fam() != "All":
            return None

        return ui.card(
            ui.card_header("Technical familiarity"),
            bar(data(input)[FAM])
        )

    @render.ui
    def frame_chart():

        frame = (
            data(input)[FRAME]
            .str.split(";")
            .explode()
            .str.strip()
        )

        return bar(frame[frame != ""])

    @render.ui
    def likert_chart():

        long = data(input).melt(
            id_vars=["Submission id"],
            value_vars=LIKERT,
            var_name="Statement",
            value_name="Response",
        )

        long = long[long.Response.isin(ORDER)]

        counts = (
            long.groupby(
                ["Statement", "Response"]
            )
            .size()
            .reset_index(name="Count")
        )

        fig = px.bar(
            counts,
            x="Statement",
            y="Count",
            color="Response",
            category_orders={
                "Response": ORDER,
                "Statement": LIKERT,
            },
            barmode="stack",
        )

        fig.update_layout(
            xaxis_tickangle=-25
        )

        return ui.HTML(
            fig.to_html(
                full_html=False,
                include_plotlyjs="cdn"
            )
        )

#----- APP ---------------------------------------------------------------

app = App(app_ui, server)