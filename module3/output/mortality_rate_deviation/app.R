library(shiny)
library(plotly)
library(dplyr)

mortalityData <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv", header=TRUE, sep=",")

# get all states 
states <- unique(mortalityData$State)

# find national population by Year

populationByYear <- mortalityData %>%
  group_by(State, Year) %>%
  summarize(Population = max(Population)) %>%
  group_by( Year) %>%
  summarize(NationalPopulation = sum(Population))

joinedData <- mortalityData %>% inner_join(populationByYear)

# find weighted average of Mortality Crude rate 

weightedAvg <- joinedData %>%
  group_by(State, Year,ICD.Chapter) %>%
  summarize(weightedCrude.Rate = Population/NationalPopulation * Crude.Rate) %>%
  group_by( Year,ICD.Chapter) %>% 
  summarize(weightedAvg = sum(weightedCrude.Rate)) 
head(weightedAvg)

# find the deviation of crude mortality from weighted average of Mortality Crude rate by year, state and cause.

finalData <- mortalityData %>% inner_join(weightedAvg) %>% mutate(Crude.Rate_deviation = Crude.Rate - weightedAvg);



# Define UI for app that draws a histogram ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("Crude Mortality Rate - Growth/Decline from National Average (1999 - 2010)"),
  
  # Drop down layout with input  ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      
      # Input: Selecter Drop down with default year as 2010
      selectInput("state", "State:",
                  states) , width = 2
      
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      
      # Output: Histogram ----
      plotlyOutput(outputId = "distPlot"), width = 9
      
    )
  )
)


# Define server logic required to draw a histogram ----
server <- function(input, output) {
  
  
  
  output$distPlot <- renderPlotly({
    filteredData <- finalData %>% filter(State == input$state ) 
    

    
    
    plot_ly(filteredData, 
            x = ~Year, 
            y = ~Crude.Rate_deviation, type = 'scatter', mode = 'lines+markers', color = ~ICD.Chapter)  %>%
      layout( width = 1500, height = 850,yaxis = list(title = 'Crude Mortality - Deviation from National Average'),
              legend = list( font = list(size = 10), orientation = 'h'))
  })
  
}
# Create Shiny app ----


shinyApp(ui = ui, server = server)

