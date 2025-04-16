let question = document.getElementById("question");
let choices = Array.from(document.getElementsByClassName("choice-text"));
let choice_containers = Array.from(document.getElementsByClassName("choice-container"));
let progressText = document.getElementById("progressText");
let scoreText = document.getElementById("score");
let progressBarFull = document.getElementById("progressBarFull");
let loader = document.getElementById("loader");
let game = document.getElementById("game");
let alert_wrong_answer = document.getElementById("alert_wrong_message");

let answer_a_container = document.getElementById("answer_a_container");
let answer_b_container = document.getElementById("answer_b_container");
let answer_c_container = document.getElementById("answer_c_container");
let answer_d_container = document.getElementById("answer_d_container");


let currentQuestion = {};
let acceptingAnswers = false;
let score = 0;
let correctAnswersCounter = 0;
let availableQuesions = [];

let questions = [];
let user_answers="";
let question_ids="";
let previous_element;
let max_questions = 3;
let pass_point  = 3;

let current_count_wrong_quesions=0;
let total_wrong_questions=0;

let start_time;
let end_time;
fetch(
  "/api/v1/quizapi/getQuestions"
)
  .then(res => {
    return res.json();
  })
  .then(loadedQuestions => {    
    load_questions(loadedQuestions);
    startGame();
  })
  .catch(err => {
    console.error(err);
  });

//CONSTANTS
const CORRECT_BONUS = 1;

startGame = () => {
//  init();
  correctAnswersCounter = 0;
  score = 0;
  availableQuesions = [...questions];
  getNewQuestion();
  hidden_loading();
  start_time = new Date();
};
load_questions = (loadedQuestions) => {
  console.log(loadedQuestions);
  max_questions = loadedQuestions.max_questions;
  if(loadedQuestions.pass_point){
    pass_point = loadedQuestions.pass_point;
  }
  console.log(pass_point);
//    console.log(loadedQuestions.results);
    questions = loadedQuestions.results.map(loadedQuestion => {
      const formattedQuestion = {
        question: loadedQuestion.question,
        question_id : loadedQuestion.question_id
      };

      const answerChoices = [...loadedQuestion.incorrect_answers];
      formattedQuestion.answer = Math.floor(Math.random() * 3) + 1;
      answerChoices.splice(
        formattedQuestion.answer - 1,
        0,
        loadedQuestion.correct_answer
      );

      answerChoices.forEach((choice, index) => {
        formattedQuestion["choice" + (index + 1)] = choice;
      });
      return formattedQuestion;
    });
};
show_loading= () =>{
  game.classList.add("hidden");
  loader.classList.remove("hidden");
};
hidden_loading = () => {
    game.classList.remove("hidden");
  loader.classList.add("hidden");
};
show_alert_wrong_answer = () => {
  alert_wrong_answer.classList.remove("hidden")
};
hidden_alert_wrong_answer = () => {
  alert_wrong_answer.classList.add("hidden")
};
getNewQuestion = () => {
  if (availableQuesions.length === 0 && correctAnswersCounter < pass_point) {
    show_loading();
    fetch(
      "/api/v1/quizapi/getQuestions"
    )
      .then(res => {
        return res.json();
      })
      .then(loadedQuestions => {    
        load_questions(loadedQuestions);
        availableQuesions = [...questions];
        getNewQuestion()
        hidden_loading();
      })
      .catch(err => {
        console.error(err);
      });
  }
  else if (availableQuesions.length === 0 || correctAnswersCounter >= pass_point) {
    show_loading();
    end_time = new Date();
    let answer_time = (end_time.getTime()- start_time.getTime())/1000
    data = {
        "correct_answer" : score,
        "answers" :user_answers,
        "questions" : question_ids,
        "wrong_answers" : total_wrong_questions,
        "answer_time" : answer_time
    };
    fetch('/api/v1/quizapi/insertAnswers', {
      method: 'POST', // or 'PUT'
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }).then(response => response.json())
        .then(data => {
//          console.log('Success:', data);
          return window.location.assign("/quizview/end");
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    //go to the end page

  }else{
      progressText.innerText = `Trả lời đúng ${correctAnswersCounter}/${pass_point}`;
      //Update the progress bar
      progressBarFull.style.width = `${(correctAnswersCounter / pass_point) * 100}%`;

      const questionIndex = Math.floor(Math.random() * availableQuesions.length);
      currentQuestion = availableQuesions[questionIndex];
      question.innerHTML = currentQuestion.question;
      question_id = currentQuestion.question_id;
      question_ids+=","+question_id;

      choices.forEach(choice => {
        const number = choice.dataset["number"];
        let content_question = currentQuestion["choice" + number];
        if(content_question){
          choice.innerHTML = content_question;
        }else{
          choice.parentElement.classList.add("hidden");
        }           

      });

      availableQuesions.splice(questionIndex, 1);
      acceptingAnswers = true;
  }

};
resetAnswersStyle= () => {
  choice_containers.forEach(
    choice_container => {
      choice_container.classList.remove("hidden");
    }
  )
}
answer_question = (id) => {
    removePreviousAnswer();
    let choice = document.getElementById(id);
    const selectedChoice = choice;
    previous_element = selectedChoice;
    const selectedAnswer = selectedChoice.dataset["number"];

    const classToApply =
      selectedAnswer == currentQuestion.answer ? "correct" : "incorrect";
    const result =
      selectedAnswer == currentQuestion.answer ? "c" : "i";
    
    if (result === "c") {
      incrementCorrectAnswers();
    }else{
      current_count_wrong_quesions+=1;
    }
    saveAnswer(result);
    incrementQuestionsCount(1);
    applyStyleForAnswer(selectedChoice, classToApply);
//    console.log(current_count_wrong_quesions)
    if(current_count_wrong_quesions==1 && (result === "i")){
      show_alert_wrong_answer();
    }else{
      current_count_wrong_quesions = 0;
      if(result === "i"){
        total_wrong_questions+=1;
      }
      runGetNewQuestion(selectedChoice, classToApply);
    }    
}
;

incrementQuestionsCount = num => {
  score += num;
  scoreText.innerText = `${score}`;
};
incrementCorrectAnswers = () => {
  correctAnswersCounter+=1;
  progressText.innerText = `Trả lời đúng ${correctAnswersCounter}/${pass_point}`;
  //Update the progress bar
  progressBarFull.style.width = `${(correctAnswersCounter / pass_point) * 100}%`;
}

function removePreviousAnswer() {
  if (previous_element) {
    previous_element.parentElement.classList.remove("incorrect");
  }
}

function runGetNewQuestion(selectedChoice, classToApply) {  
  setTimeout(() => {
    previous_element = null;
    hidden_alert_wrong_answer();
    selectedChoice.parentElement.classList.remove(classToApply);
    resetAnswersStyle(); 
    getNewQuestion();
  }, 500);
}

function applyStyleForAnswer(selectedChoice, classToApply) {
  selectedChoice.parentElement.classList.add(classToApply);  
}

function saveAnswer(r) {
//  console.log(currentQuestion);
  user_answers += "," + currentQuestion.question_id + ":" + r;
//  console.log("a=" + user_answers);
}
