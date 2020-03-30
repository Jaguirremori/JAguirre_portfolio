#Jose Aguirre-Mori

library(car)
library(descr)
library(DescTools)
library(summarytools)
library(PerformanceAnalytics) # for chart.Correlation
library(stargazer) # for regression table outputs
library(plyr)
library(ggplot2)

#Load imdb database 
mov <- read.csv(file.choose(), header = T)
#Subset to remove any rows where gross = NA
#Idk how to do this any other way
mov.us <- subset(mov, mov$gross != "NA")
mov.us2 <- subset(mov.us, mov.us$budget != "NA")
mov.us3 <- subset(mov.us2, mov.us2$num_voted_users != "NA")
mov.us4 <- subset(mov.us3, mov.us3$duration != "NA")
mov.us5 <- subset(mov.us4, mov.us4$cast_total_facebook_likes != "NA")
#gather the descriptive statistics
descr::descr(mov.us5$gross)
descr::descr(mov.us5$num_voted_users)
descr::descr(mov.us5$budget)
descr::descr(mov.us5$duration)
descr::descr(mov.us5$cast_total_facebook_likes)
sd(mov.us5$num_voted_users, na.rm=TRUE)
sd(mov.us5$gross, na.rm=TRUE)
sd(mov.us5$budget, na.rm=TRUE)
sd(mov.us5$cast_total_facebook_likes, na.rm=TRUE)
sd(mov.us5$duration, na.rm =TRUE)


#SCALING
gross_sc2  = mov.us5$gross/1000000
num_vote_sc2 = mov.us5$num_voted_users/2200
budget_sc2 = mov.us5$budget/1000000
facebook_likes2=  mov.us5$cast_total_facebook_likes/1000
#Inserting into regression model
help <- lm(gross_sc2 ~ mov.us5$duration + num_vote_sc2 + budget_sc2 + facebook_likes2)
#Diagnostic Plots
plot(help)
#Vif
vif(help)
summary(help)

model1 <- help
stargazer(model1, type= "html", out = "output.html")

#extra credit plot
ggplot(mov.us5, aes(x = facebook_likes2, y = gross_sc2, color = budget_sc2, lwd = num_vote_sc2)) + geom_point() + geom_abline()


