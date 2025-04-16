let question = document.getElementById("question");
let choices = Array.from(document.getElementsByClassName("choice-text"));
let choice_containers = Array.from(document.getElementsByClassName("choice-container"));
let choice_selects = Array.from(document.getElementsByClassName("choice-select"));
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

// let answer_containers = [answer_a_container, answer_b_container, answer_c_container, answer_d_container];

let multi_select_button = document.getElementById("multi_select_button");


let currentQuestion = {};
let acceptingAnswers = false;
let count_questions = 0;
let correctAnswersCounter = 0;
let availableQuesions = [];

let questions = [];
let user_answers = "";
let question_ids = "";
let max_questions = 5;
let pass_point = 5;

let current_count_wrong_quesions = 0;
let total_wrong_questions = 0;

let start_time;
let end_time;

let current_question_type;
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

function startGame() {
  //  init();
  correctAnswersCounter = 0;
  count_questions = 1;
  availableQuesions = [...questions];
  getNewQuestion();
  hidden_loading();
  start_time = new Date();
};

function load_questions(loadedQuestions) {
  max_questions = loadedQuestions.max_questions;
  if (loadedQuestions.pass_point) {
    pass_point = loadedQuestions.pass_point;
  };
  questions = loadedQuestions.results.map(loadedQuestion => {
    var q_type = loadedQuestion.type;
    if (q_type) {
      q_type = q_type.trim().toLocaleLowerCase();
    }
    const formattedQuestion = {
      question: loadedQuestion.question,
      question_id: loadedQuestion.question_id,
      type: q_type
    };
    if(q_type == 'single choice'){
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
    }else if(q_type == 'multi choice'){
      const answerChoices = [...loadedQuestion.incorrect_answers];
      
      loadedQuestion.correct_answer.forEach(
        (correct_answer) => {
          var aid = Math.floor(Math.random() * 3) + 1;
          answerChoices.splice(
            aid - 1,
            0,
            correct_answer
          );
        }
      );

      answerChoices.forEach((choice, index) => {
        formattedQuestion["choice" + (index + 1)] = choice;
      });
      formattedQuestion.answer=[];
      loadedQuestion.correct_answer.forEach(
        (correct_answer) => {
          var idx = answerChoices.indexOf(correct_answer)+1;
          formattedQuestion.answer.push(idx+"");
        }
      );
    }
    
    return formattedQuestion;
  });
  console.log(questions);
};
function show_loading() {
  game.classList.add("hidden");
  loader.classList.remove("hidden");
};
function hidden_loading() {
  game.classList.remove("hidden");
  loader.classList.add("hidden");
};
function show_alert_wrong_answer() {
  alert_wrong_answer.classList.remove("hidden")
};
function hidden_alert_wrong_answer() {
  alert_wrong_answer.classList.add("hidden")
};
function getNewQuestion() {
  // if not pass and not has more available questions -> load more question from server
  if (availableQuesions.length === 0 && correctAnswersCounter < pass_point) {
    show_loading();
    load_new_questions();
  }
  // if pass examp -> post answer to server
  else if (availableQuesions.length === 0 || correctAnswersCounter >= pass_point) {
    show_loading();
    postAnswer();
    //go to the end page

  }
  // load next question in available questions
  else {
    update_processbar();
    load_question();
  }

};
function resetAnswersStyle() {
  choice_containers.forEach(
    choice_container => {
      choice_container.classList.remove("hidden");
      choice_container.classList.remove("correct");
      choice_container.classList.remove("incorrect");
      choice_container.classList.remove("answer_selected");
      choice_container.classList.remove("answer_selected_color");
      choice_container.getElementsByClassName("select-box")[0].checked=false;
    }
  )
}
function hide_answer_button() {
  multi_select_button.classList.add("hidden");
  choice_selects.forEach(
    (choice_select) => {
      if(!choice_select.classList.contains("hidden")){
        choice_select.classList.add("hidden");
      }      
    }
  );
}
function show_answer_button() {
  multi_select_button.classList.remove("hidden");
  choice_selects.forEach(
    (choice_select) => {
      choice_select.classList.remove("hidden");      
    }
  );
}
function answer_question(id) {
  if (current_question_type == 'single choice') {
    removePreviousAnswer();
    const selectedChoice = document.getElementById(id);
    const result = computeResultForSG(selectedChoice);
    applyStyleToAnswer(result, selectedChoice);
    increaseWrongQuestion(result);
    saveAnswer(result);
    if (current_count_wrong_quesions == 1 && (result === "i")) {
      show_alert_wrong_answer();
    }
    else {
      incrementQuestionsCount(1);
      next_question(result);
    }
  } else if (current_question_type == 'multi choice') {
    console.log("answer multi choice question " + id);
    let choice = document.getElementById(id);
    const selectedChoice = choice;
    if (selectedChoice.parentElement.classList.contains("answer_selected")) {
      selectedChoice.parentElement.classList.remove("answer_selected");
      selectedChoice.parentElement.getElementsByClassName("select-box")[0].checked=false;
      selectedChoice.parentElement.classList.remove("answer_selected_color");
      if(selectedChoice.parentElement.classList.contains("incorrect")
      || selectedChoice.parentElement.classList.contains("correct")
      ){
        selectedChoice.parentElement.classList.remove("incorrect");
        selectedChoice.parentElement.classList.remove("correct");
      }
    } else {
      selectedChoice.parentElement.classList.add("answer_selected");
      selectedChoice.parentElement.classList.add("answer_selected_color");
      selectedChoice.parentElement.getElementsByClassName("select-box")[0].checked=true;
      
    }

  }

}

function computeResultForSG(selectedChoice) {
  const selectedAnswer = selectedChoice.dataset["number"];
  const result = selectedAnswer == currentQuestion.answer ? "c" : "i";
  return result;
}

function applyStyleToAnswer(result, selectedChoice) {
  const classToApply = result == 'c' ? "correct" : "incorrect";
  selectedChoice.parentElement.classList.remove("answer_selected_color");
  selectedChoice.parentElement.classList.add(classToApply);
}

function increaseWrongQuestion(result) {
  if (result === "c") {
    incrementCorrectAnswers();
  }
  else {
    current_count_wrong_quesions += 1;
  }
}

function next_question(result) {
  current_count_wrong_quesions = 0;
  if (result === "i") {
    total_wrong_questions += 1;
  }
  runGetNewQuestion();
}

function answer_question_multi() {
  removePreviousAnswer();
  var count_corrrect_answers = 0;
  var count_incorrect_answers=0;
  choice_containers.forEach(
    (choice_container) => {
      if(choice_container.classList.contains("answer_selected")){
        var selectedChoice = choice_container.getElementsByClassName("choice-text")[0];
        const selectedAnswer = selectedChoice.dataset["number"];
        // var result = "i";
        if(currentQuestion.answer.indexOf(selectedAnswer)>-1){
          // result = "c";
          count_corrrect_answers+=1;
        }else{
          count_incorrect_answers+=1;
        }
        // applyStyleToAnswer(result, selectedChoice);
      }
      
    }
  );

  var result= "i";
  if(count_corrrect_answers== currentQuestion.answer.length && count_incorrect_answers==0){
    result = "c";
  }
  choice_containers.forEach(
    (choice_container) => {
      if(choice_container.classList.contains("answer_selected")){
        var selectedChoice = choice_container.getElementsByClassName("choice-text")[0];
        applyStyleToAnswer(result, selectedChoice);
      }
      
    }
  );
  increaseWrongQuestion(result);
  saveAnswer(result);  
  if (current_count_wrong_quesions == 1 && (result === "i")) {
    show_alert_wrong_answer();
  }
  else {
    incrementQuestionsCount(1);
    next_question(result);  
  }
}

function incrementQuestionsCount(num) {
  count_questions += num;
  scoreText.innerText = `${count_questions}`;
};
function incrementCorrectAnswers() {
  correctAnswersCounter += 1;
  progressText.innerText = `Trả lời đúng ${correctAnswersCounter}/${pass_point}`;
  //Update the progress bar
  progressBarFull.style.width = `${(correctAnswersCounter / pass_point) * 100}%`;
}

function load_question() {
  const questionIndex = Math.floor(Math.random() * availableQuesions.length);
  currentQuestion = availableQuesions[questionIndex];
  question.innerHTML = currentQuestion.question;
  question_id = currentQuestion.question_id;
  question_ids += "," + question_id;
  current_question_type = currentQuestion.type;

  choices.forEach(choice => {
    const number = choice.dataset["number"];
    let content_question = currentQuestion["choice" + number];
    if (content_question) {
      choice.innerHTML = content_question;
    }
    else {
      choice.parentElement.classList.add("hidden");
    }

  });

  availableQuesions.splice(questionIndex, 1);
  acceptingAnswers = true;

  if (current_question_type == 'single choice') {
    hide_answer_button();
  } else if (current_question_type == 'multi choice') {
    show_answer_button();
  }
}

function update_processbar() {
  progressText.innerText = `Trả lời đúng ${correctAnswersCounter}/${pass_point}`;
  //Update the progress bar
  progressBarFull.style.width = `${(correctAnswersCounter / pass_point) * 100}%`;
}

function postAnswer() {
  end_time = new Date();
  let answer_time = (end_time.getTime() - start_time.getTime()) / 1000;
  data = {
    "correct_answer": count_questions,
    "answers": user_answers,
    "questions": question_ids,
    "wrong_answers": total_wrong_questions,
    "answer_time": answer_time
  };
  fetch('/api/v1/quizapi/insertAnswers', {
    method: 'POST',
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
}

function load_new_questions() {
  fetch(
    "/api/v1/quizapi/getQuestions"
  )
    .then(res => {
      return res.json();
    })
    .then(loadedQuestions => {
      load_questions(loadedQuestions);
      availableQuesions = [...questions];
      getNewQuestion();
      hidden_loading();
    })
    .catch(err => {
      console.error(err);
    });
}

function removePreviousAnswer() {
  choice_containers.forEach(
    choice_container => {
      choice_container.classList.remove("correct");
      choice_container.classList.remove("incorrect");
    }
  )
}

function runGetNewQuestion() {
  setTimeout(() => {
    hidden_alert_wrong_answer();
    resetAnswersStyle();
    getNewQuestion();
  }, 500);
}


function saveAnswer(r) {
  //  console.log(currentQuestion);
  user_answers += "," + currentQuestion.question_id + ":" + r;
  //  console.log("a=" + user_answers);
}
