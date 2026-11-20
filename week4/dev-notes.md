# Building a TfL Shiny dashboard

Welcome to you shiny new dataviz project. We will build a Shiny app over four sessions across Weeks 4 and 5. You will have the two Thursday labs to apply what you have learned to own projects.

| Session | What we will build |
|---|---|
| 4.1 | An app that runs: UI, server, inputs, one output, first API call |
| 4.2 | Live data on screen: a reactive calculation, a table, a chart, a filter |
| 4.3 Lab | The same pattern on your own project data |
| 5.1 | Inputs that depend on other inputs, a second data source, error handling |
| 5.2 | Layout, then deployment to the web |
| 5.3 Lab | Your own app, deployed |

We build the app live, from an empty `app.py`. Type along: you will remember the errors better than just reading the working version. Remember, we learn from discomfort.

---

## 4.1 An app that runs

1. **Hello Shiny** (Core, not Express)
    - [x] Start from an empty `app.py`. Write the three parts: `app_ui`, `server(input, output, session)`, `app = App(app_ui, server)`.
    - [x] Run it with `shiny run --reload app.py` and open it in your browser.
    - [x] Add one `ui.input_slider` and one `ui.output_text`, and the `@render.text` function behind it.
    - [x] Change the value in the browser and watch the text update. You never told it to refresh: that is the whole idea.
    - [x] Change the layout to `ui.page_sidebar()`, and give a title to the sidebar and to the main panel.
    - [x] Add a `ui.input_select` dropdown.

2. **A first API call, outside Shiny**
    - [x] In a scratch notebook, call `https://api.tfl.gov.uk/line/mode/tube/status` with `requests`.
    - [x] Turn the response into Python with `.json()` and store it in `data`.
    - [x] Print it, and find where the line name and the status description are hiding inside the nesting.

3. **The same call, inside the app**
    - [x] Write `network_status()`, which fetches the line statuses and returns `r.json()`.
    - [x] Write `health_badge()`, rendered with `@render.text`, showing the status of the first line.

**Checkpoint:** your app shows one line's status, fetched live.

---

## 4.2 Live data on screen

4. **A table**
    - [ ] Try the obvious thing first: `pd.DataFrame(data)` inside `network_status()`, return it, and render it with `@render.table` in a function called `status_table()`. Look at what appears on the page.
    - [ ] It is unreadable, because one column holds a list of dictionaries. Print `data[0]` in your scratch notebook and find where the status actually lives: inside `lineStatuses`, which is a **list**, whose first entry has `statusSeverityDescription` and sometimes `reason`.
    - [ ] Build the table yourself instead. Loop over the lines, and for each one collect three things into a dictionary: the line `name`, the first status's `statusSeverityDescription`, and its `reason`. Append each dictionary to a list called `rows`.
    - [ ] Use `.get("reason")` rather than `["reason"]`: a line with a good service has no reason, and square brackets would crash the app.
    - [ ] Return `pd.DataFrame(rows)`. You should get eleven rows and three columns: `line`, `status`, `reason`.
    - [ ] Now `health_badge()` can read `df["status"]` instead of digging through nested lists. Simplify it.
    - [ ] Two of your outputs now use `network_status()`. Add `print(">>> calling the API", flush=True)` as its first line, reload the page, and count the lines in your terminal.
    - [ ] Add the `@reactive.calc` decorator and reload again. One print instead of two: that is what it saved you.

5. **A summary and a chart**
    - [ ] Change `health_badge()` to count the lines on "Good Service" against the total.
    - [ ] Write `status_plot()`, counting each status, rendered with `@render.plot`.

6. **A filter that changes the data**
    - [ ] Add a `ui.input_checkbox_group` for modes: tube, dlr, overground.
    - [ ] Make `network_status()` depend on `input.modes()`.
    - [ ] Tick a box, and watch the table and the chart both update from one input.

**Checkpoint:** a live table, a health summary and a bar chart, all filtered by mode.

---

## 4.3 Lab: your own data, on screen

No new material. The same steps as 4.1 and 4.2, on the dataset for your project.

This is project work, so it belongs in `project/`, not in a week folder. Everything you
build today is part of what you submit.

- [ ] Pick the dataset you will use for your project. A CSV is fine, an API is fine.
- [ ] Create `project/app.py` and build an app with one input and one output: a filter, and a table or a plot of your data.
- [ ] Make a second output depend on the same reactive calculation.
- [ ] Say in `project/README.md` where the data comes from and how someone else would get it.
- [ ] Commit `project/` and push.

If you have not chosen your dataset yet, choose it today. Your project needs data well before Week 7, and an afternoon spent plotting it tells you more about whether it will work than another week of thinking about it.

**Where your data file goes.** `data/` is in `.gitignore`, so anything you put there stays
on your laptop and never reaches GitHub. That is deliberate: data files are usually large,
often licensed, and sometimes personal. Read from `data/` while you are working, and
describe in the README how to obtain it. We deal with what this means for a deployed app
in 5.3.

---

## 5.1 Inputs that depend on inputs

7. **A dropdown that fills itself**
    - [ ] Add `ui.input_select("line")`, starting empty.
    - [ ] Write `_populate_lines()`, which calls `/line/mode/{modes}` and fills the dropdown with `ui.update_select`.
    - [ ] Decorate it with `@reactive.Effect`. An Effect changes something; a Calc returns something. Which one did you need here, and why?

8. **A second one, depending on the first**
    - [ ] Add `ui.input_select("station")`.
    - [ ] Write `_populate_stations()`, which calls `/line/{line_id}/stoppoints` when the line changes.
    - [ ] Add `@reactive.event(input.line)` so it only fires when the line changes. Take it off again and see what your app starts doing.

9. **A second endpoint: the arrivals board**
    - [ ] Add a `ui.input_slider("n_arrivals")`.
    - [ ] Write `arrivals_table()`, calling `/StopPoint/{station}/arrivals` and keeping `lineName`, `platformName`, `destinationName` and `timeToStation`.
    - [ ] Sort by time and show the next N.

10. **When the network is not there**
    - [ ] Put `try`/`except` around your API calls.
    - [ ] Show a message in the UI instead of a stack trace when a call fails.
    - [ ] Turn off your wifi and check that you were right.

11. **A refresh button**
    - [ ] Add a `ui.input_action_button("refresh")`.
    - [ ] Make the API calls depend on the button as well as on the inputs.

**Checkpoint:** choosing a line changes the stations, choosing a station shows arrivals, and a dead API no longer kills your app.

---

## 5.2 Layout, and putting it on the web

12. **Layout**
    - [ ] Arrange the main panel with `ui.layout_columns` and `ui.card`.
    - [ ] Top row: network health and the bar chart. Middle: arrivals. Bottom: disruptions.
    - [ ] Sidebar: modes, line, station, arrivals slider, refresh.

13. **A disruptions panel**
    - [ ] Write `disruptions_panel()`, calling `/StopPoint/{station}/disruption`.
    - [ ] Render a bullet list with `ui.tags.ul` and `ui.tags.li`, or "No disruptions" when there are none.

14. **Declare what your app needs**
    - [ ] `pip freeze` is not the answer. Write `requirements.txt` by hand: the packages you import, and nothing else.
    - [ ] Test it. New virtual environment, `pip install -r requirements.txt`, run the app.
    - [ ] Deployment is the moment an undeclared dependency stops being your problem and becomes everyone else's.

15. **Deploy it, two ways**

    **a. Posit Connect Cloud.** Your app runs on a server, so the TfL calls work.
    - [ ] Push the app to a public GitHub repository, with `app.py` and `requirements.txt` at the root.
    - [ ] Sign in to connect.posit.cloud with GitHub, pick the repository, deploy.
    - [ ] Open the public URL on your phone.

    **b. GitHub Pages, via shinylive.** No server: your app runs inside the visitor's browser.
    - [ ] `pip install shinylive`, then `shinylive export . docs/`
    - [ ] Push, then switch GitHub Pages on for the `docs/` folder in your repository settings.
    - [ ] Free and permanent, with two limits you need to know: every package has to work in the browser under Pyodide, and API calls go through the browser's cross-origin rules, so a live API can be blocked even though it works on your laptop.

    Which one should you use? Static export if your app reads a CSV you ship with it. Posit Connect Cloud if it calls an API or reads a database.

**Checkpoint:** your dashboard has a URL you can send to someone else.

---

## 5.3 Lab: deploy your own

Still project work, still in `project/`.

- [ ] Extend `project/app.py` with a second view: another plot, or a table beside the chart.
- [ ] Write `requirements.txt` by hand, at the repository root, and test it in a clean environment.
- [ ] Deploy it, by whichever of the two routes suits your data.
- [ ] Put the URL in `project/README.md`, and commit.

**Your deployed app cannot read `data/`.** Nothing in that folder is on GitHub, so a
deployed app will start and then fail the moment it tries to load the file. Three ways out,
in order of preference:

1. **Call the source directly**, if your data comes from an API or a public URL.
2. **Commit a small extract** to `project/app-data/`, a few hundred rows, enough for the
   app to show what it does. Say in the README that it is an extract, and check the licence
   allows you to publish it.
3. **Do not deploy this one.** If the data cannot be published, say so in the README and
   demonstrate the app locally instead. That is a legitimate answer, and a better one than
   quietly pushing data you do not have the right to share.

---

## Stretch, if you finish early

- [ ] A journey planner: `/Journey/JourneyResults/{from}/to/{to}`, with two station dropdowns and a button.
- [ ] Cache the API responses for a few seconds, so a refresh does not hammer the endpoint.
- [ ] A map, with `shinywidgets` and `ipyleaflet`.
