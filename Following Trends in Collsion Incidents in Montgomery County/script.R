#load packages
library(readr)
library(dplyr)
library(stringr)
library(purrr)
library(lubridate)

#read in csv
incidents <- read_csv("moco_crash_incident.csv")
head(incidents)

#convert crashdate and time to date time
incidents$date_only <- strptime(as.character(incidents$`Crash Date/Time`), "%m/%d/%Y")
incidents$date_only <- as.Date(incidents$date_only, format = "%m/%d/%Y")
typeof(incidents$date_only)



#inject date_only column and crash occurance into df
incidents <- incidents %>% mutate(date_only = date_only, crash_count = 1)

#make a groupby date_only and sum the crash_count 
#column so that crash_count = total number accidents for that date
crash_count_data <- incidents %>% 
  group_by(date_only) %>% 
  summarize(crash_occurences = sum(crash_count))

#create df of last three years in march from the first to the 19th
march <- subset(crash_count_data, date_only >= "2020-03-01" & date_only <= "2020-03-19"
                |date_only >= "2019-03-01" & date_only <= "2019-03-19" 
                |date_only >= "2018-03-01" & date_only <= "2018-03-19")

write_csv(march, "moco_crashes_march.csv")

