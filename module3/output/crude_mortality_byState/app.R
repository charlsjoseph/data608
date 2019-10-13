library(shiny)
library(plotly)
library(dplyr)

mortalityData <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv", header=TRUE, sep=",")

years <- unique(mortalityData$Year)
Causes <- unique(mortalityData$ICD.Chapter)

# Define UI for app that draws a histogram ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("Mortality - Crude Rates in United States (1999 - 2010) "),
  
  # Drop down layout with input  ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      
      # Input: Selecter Drop down with default year as 2010
      selectInput("year", "Year:",
                  years, 2010),
      actionLink("togglebtton","Select/Deselect All"),
      checkboxGroupInput("cause", "Causes:",
                         Causes, Causes) , width = 3
      
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      
      # Output: Histogram ----
      plotlyOutput(outputId = "distPlot"), width = 9
      
    )
  )
)


# Define server logic required to draw a histogram ----
server <- function(input, output, session) {
  
  observe({
    if (input$togglebtton%%2 == 0)
    {
      updateCheckboxGroupInput(session, "cause", "Causes:",
                               Causes, Causes)
    }
    else
    {
      updateCheckboxGroupInput(session, "cause", "Causes:",
                               Causes)
    }
  })
  
  
  output$distPlot <- renderPlotly({
    filteredData <- mortalityData %>% filter(Year == input$year & ICD.Chapter %in%  input$cause) 
    mortalityDataByState <- filteredData %>%
      group_by(State) %>%
      summarize(totalrate = sum(Crude.Rate, na.rm = TRUE)) 
    filteredData <- filteredData %>% inner_join(mortalityDataByState)
    
    
    
    
    plot_ly(filteredData, 
            x = ~reorder(State, -totalrate), 
            y = ~Crude.Rate, 
            text = ~Crude.Rate,  
            type = 'bar', 
            color = ~reorder(ICD.Chapter, -Crude.Rate) )  %>%
      layout( width = 1400, height = 850,  
              yaxis = list(title = 'Crude Mortality Rate', font = list(size = 10)), 
              xaxis = list(title = 'State', font = list(size = 10)) , 
              barmode = 'stack', 
              legend = list( font = list(size = 10), orientation = 'h'))
  })
  
}
# Create Shiny app ----


shinyApp(ui = ui, server = server)

