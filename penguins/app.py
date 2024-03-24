import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import render, reactive
import palmerpenguins
import seaborn as sns

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Palmer Penguins: Hansen", fillable=True)

# Add a Shiny UI sidebar for user interaction
# Use the ui.sidebar() function to create a sidebar
# Set the open parameter to "open" to make the sidebar open by default
# Use a with block to add content to the sidebar
with ui.sidebar(open="open"):
    # Use the ui.h2() function to add a 2nd level header to the sidebar
    #   pass in a string argument (in quotes) to set the header text to "Sidebar"
    ui.h2("Sidebar")

    # Use ui.input_selectize() to create a dropdown input to choose a column
    #   pass in three arguments:
    #   the name of the input (in quotes), e.g., "selected_attribute"
    #   the label for the input (in quotes)
    #   a list of options for the input (in square brackets)
    #   e.g. ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    ui.input_selectize(
        "selected_attribute",
        "Select Attribute for Histograms:",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    #   pass in two arguments:
    #   the name of the input (in quotes), e.g. "plotly_bin_count"
    #   the label for the input (in quotes)
    ui.input_numeric("plotly_bin_count", "Bin Count for Plotly Chart", 5)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    #   pass in four arguments:
    #   the name of the input (in quotes), e.g. "seaborn_bin_count"
    #   the label for the input (in quotes)
    #   the minimum value for the input (as an integer)
    #   the maximum value for the input (as an integer)
    #   the default value for the input (as an integer)
    ui.input_slider("seaborn_bin_count", "Bin Count for Seaborn Chart", 0, 20, 5)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    #   pass in five arguments:
    #   the name of the input (in quotes), e.g.  "selected_species_list"
    #   the label for the input (in quotes)
    #   a list of options for the input (in square brackets) as ["Adelie", "Gentoo", "Chinstrap"]
    #   a keyword argument selected= a list of selected options for the input (in square brackets)
    #   a keyword argument inline= a Boolean value (True or False) as you like
    ui.input_checkbox_group(
        "selected_species",
        "Select Species:",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True,
    )

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.a() to add a hyperlink to the sidebar
    #   pass in two arguments:
    #   the text for the hyperlink (in quotes), e.g. "GitHub"
    #   a keyword argument href= the URL for the hyperlink (in quotes), e.g. your GitHub repo URL
    #   a keyword argument target= "_blank" to open the link in a new tab
    ui.a(
        "My GitHub Repo",
        href="https://github.com/nhansen23/cintel-02-data",
        target="_blank",
    )

# When passing in multiple arguments to a function, separate them with commas.

with ui.layout_columns():
    with ui.card():
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            # Create a Plotly scatterplot using Plotly Express
            # Call px.scatter() function
            # Pass in six arguments
            return px.scatter(
                data_frame=filtered_data(),
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                labels={
                    "bill_depth_mm": "Bill Depth (mm)",
                    "body_mass_g": "Body Mass (g)"
                },
                size_max=8,
            )
    
    with ui.navset_card_underline(title="Histograms"):
        with ui.nav_panel("Plotly Histogram"):
            @render_plotly
            def penguins_plot1():
                return px.histogram(
                filtered_data(), x=input.selected_attribute(), nbins=input.plotly_bin_count()
                )

        with ui.nav_panel("Seaborn Histogram"):
            @render.plot
            def penguins_plot2():
                return sns.histplot(
                    data=filtered_data(),
                    x=input.selected_attribute(),
                    bins=input.seaborn_bin_count(),
                )

with ui.navset_card_underline(title="Data"):
    with ui.nav_panel("Data Grid"):
        @render.data_frame
        def penguins_df1():
            return render.DataGrid(filtered_data())
    with ui.nav_panel("Data Table"):
        @render.data_frame
        def penguins_df2():
            return render.DataTable(filtered_data())

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    filtered_rows = penguins_df["species"].isin(input.selected_species())
    return penguins_df[filtered_rows]
