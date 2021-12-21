library(caret)

xgbtrain <- function(data, sampling=NULL){
  
  #10 folds repeat 3 times
  control <- trainControl(method='repeatedcv', 
                          number=10, 
                          repeats=3,
                          #search = 'random',
                          sampling= sampling)
  
  tune_grid <- expand.grid(nrounds=c(200), 
                           max_depth = c(3),
                           eta = c(0.05),
                           gamma = c(0.01),
                           colsample_bytree = c(0.5),
                           subsample = c(0.65),
                           min_child_weight = c(20))
  
  xgb <- train(yes~., 
               data=data, 
               method='xgbTree', 
               metric='Accuracy', 
               tuneGrid=tune_grid, 
               trControl=control)
  
  return(xgb)
}

evaluation <- function(model, test){
  
  pred <- predict.train(model, newdata = test)
  probs <- predict.train(model, test, type="prob")
  
  test.df <- cbind.data.frame(pred,probs, test$yes)
  colnames(test.df) <- c("pred", colnames(probs), "obs")
  
  test.df$pred <- factor(test.df$pred, levels=c(TRUE, FALSE))
  test.df$obs <- factor(test.df$obs, levels=c(TRUE, FALSE))
  
  conf <- confusionMatrix(data = test.df$pred, reference = test.df$obs, mode = "everything")
  roc <- twoClassSummary(data = test.df, lev = levels(test.df$obs))
  
  print(conf)
  print(roc)
  
  perf <- c(roc[1], conf$overall[c(1,3,4)], conf$byClass)
  names(perf)[1] <- "AUC"
  return(list(perf=perf, table=conf$table))
  
}

c <- read.csv("performalist_voting.csv", sep=";")

features <- c[,-c(1,10)]
features$Performalist <- ifelse(features$Performalist>0,1,0)
features$yes <- as.factor(ifelse(c$`Change Point`=="true_positive",T,F))

results <- c()
for(i in 1:10){
  n <- round(nrow(diff.features)*0.9)
  ind <- sample(1:nrow(diff.features),n)
  
  train <- features[ind,-1]
  #train$distance <- NULL
  test <- features[-ind,-1]
  #test$distance <- NULL
  model <- xgbtrain(train)
  results <- rbind(evaluation(model, test)$perf)
}

