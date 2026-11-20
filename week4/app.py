from shiny import ui, render, App
import requests
import json

# ---------------- UI ----------------
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "status_filter",
            "Select Service Status",
            choices=[
                "Good Service",
                "Minor Delays",
                "Severe Delays",
                "Part Suspended",
                "No Service / Entire Line Suspended",
                "Reduced Service"],
            selected="Good Service"),),

    ui.page_fluid(
        ui.h1("TfL Tube Status Dashboard"),
        ui.output_text_verbatim("filtered_status"),))

# ---------------- SERVER ----------------
def server(input, output, session):

    @render.text
    def filtered_status():
        try:
            url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            selected_status = input.status_filter()

            # Map TfL descriptions to our categories
            mapping = {
                "Good Service": "Good Service",
                "Minor Delays": "Minor Delays",
                "Severe Delays": "Severe Delays",
                "Part Suspended": "Part Suspended",
                "No Service": "No Service / Entire Line Suspended",
                "Service Closed": "No Service / Entire Line Suspended",
                "Reduced Service": "Reduced Service"}

            results = []
            for line in data:
                name = line.get("name", "Unknown")
                if line.get("lineStatuses"):
                    description = line["lineStatuses"][0].get("statusSeverityDescription", "Unknown")
                    category = mapping.get(description, "Heavily Disrupted")
                    if category == selected_status:
                        results.append(f"{name}: {description}")

            if results:
                return "\n".join(results)
            else:
                return f"No lines with '{selected_status}'."

        except requests.exceptions.RequestException as e:
            return f"Error fetching TfL data: {e}"
        except json.JSONDecodeError:
            return "Error decoding TfL API response."

# ---------------- APP ----------------
app = App(app_ui, server)
