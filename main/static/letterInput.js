$(document).ready(function () {
	
//	var questionBank=new Array;
	var questionBank= [['עמקשלי', 'כל הכבוד הצלחתם'], [70401003003010,'נשאר לכם עוד צעד אחד לפתרון']];
	var wordArray=new Array;
	var previousGuesses=new Array;
 	var currentWord, almost;
	var currentClue, almostAnswer;
	var wrongAnswerCount;
	titleScreen();
 
 
// 		$.getJSON('quizbank.json', function(data) {
//
//		for(i=0;i<data.wordlist.length;i++){
//			questionBank[i]=new Array;
//			questionBank[i][0]=data.wordlist[i].word;
//			questionBank[i][1]=data.wordlist[i].clue;
//		}
//		titleScreen();
//		})//gtjson
 
function titleScreen(){
	$('#gameContent').append('<div id="gameTitle">הפתרון</div><div id="startButton" class="button">התחילו</div>');
	$('#startButton').on("click",function (){gameScreen()});
}//display game
	
	
	
function gameScreen(){
	$('#gameContent').empty();
	//$('#gameContent').append('<div id="pixHolder"><img id="hangman" src="man.png"></div>');
	$('#gameContent').append('<div id="wordHolder"></div>');
	$('#gameContent').append('<div id="clueHolder"></div>');
	$('#gameContent').append('<div id="guesses">נסיונות:</div>');
	$('#gameContent').append('<div id="feedback"></div>');
	//$('#gameContent').append('<form><input type="text" id="dummy" ></form>');
			
	getWord();
	var numberOfTiles=currentWord.length;
	wrongAnswerCount=0;
	previousGuesses=[];
			 
	for(i=0;i<numberOfTiles;i++){
	    if (i == 2){
	        $('#wordHolder').append('<input class="tile" id=t'+i+'>');
	        $('#wordHolder').append('<div class="tile"> - </div>');
	    }else{
	        $('#wordHolder').append('<input class="tile" id=t'+i+'>');
	    }

	}
	$('#feedback').append("<br><br><a id='check' class='button'>בדוק</a>");
	$('#check').on("click",function (){
	    //console.log('here')
		checkAnswer();
	});
			
//	$('#clueHolder').append("HINT: "+currentClue);
 
 	
//	$(document).on("keypress",handleKeyUp);
//	$(document).on("click",function(){$('#dummy').focus();});
//	$('#dummy').focus();
}//gamescreen
			
			
function getWord(){
	var rnd=Math.floor(Math.random()*questionBank.length);
	currentWord=questionBank[0][0];
	currentClue=questionBank[0][1];
	almost = questionBank[1][0];
	almostAnswer = questionBank[1][1];
	questionBank.splice(rnd,1); 
	wordArray=currentWord.split("");
	console.log("word array: "+wordArray)
}//getword
			

			
			
function handleKeyUp(event) {

	//this line deals with glitch in recent versions of android
	//if(event.keyCode==229){event.keyCode=$('#dummy').val().slice($('#dummy').val().length-1,$('#dummy').val().length).toUpperCase().charCodeAt(0);}
		
//	if(event.keyCode>64 && event.keyCode<188){
		var found=false;
		var previouslyEntered=false;
//		var input=String.fromCharCode(event.keyCode).toLowerCase();
        var charCode = event.which; // charCode will contain the code of the character inputted
        var input = String.fromCharCode(charCode); // theChar will contain the actual character
		console.log('key: '+ input)
		
	
		for(i=0;i<previousGuesses.length;i++){if(input==previousGuesses[i]){previouslyEntered=true;}}
				
		if(!previouslyEntered){
			previousGuesses.push(input);
			for(i=0;i<wordArray.length;i++){
				if(input==wordArray[i]){found=true;$('#t'+i).append(input);}	
			}//for
				
			if(found){checkAnswer();}
			else{wrongAnswer(input);}
		}//if
//	}//if
}//handlekeyup
	

function checkAnswer(){
	var currentAnswer="";	
	for(i=(currentWord.length)-1;i>=0;i--){
	    //console.log(i)
	    //console.log($('#t'+i).val())
		currentAnswer+=($('#t'+i).val());
	}
	console.log(currentAnswer)
	console.log(almost)
	console.log(almost==currentAnswer)
	console.log(currentWord==currentAnswer)
	if(currentAnswer==currentWord){
		victoryMessage(currentClue, 1);
	}else if (currentAnswer==almost){
	    victoryMessage(almostAnswer);
	}else{
	    wrongAnswer();
    };
}//checkanswer
		
function wrongAnswer(){
	wrongAnswerCount++;
	$('#feedback').empty();
	$('#feedback').append("<br>נסו שוב<br>");
//	var pos=(wrongAnswerCount*-75) +"px"
//	$('#guesses').append("  "+a);
//	$('#hangman').css("left",pos);
//	if(wrongAnswerCount==6){
//		defeatMessage();}
}//wronganswer
		
function victoryMessage(message, end){
	//document.activeElement.blur();
	//$(document).off("keyup", handleKeyUp);
	$('#feedback').empty();
	$('#feedback').append(message);
    $('#feedback').append("<br><br><a id='check' class='button'>בדוק</a>");
    $('#check').on("click",function (){
	    //console.log('here')
		checkAnswer();
	});
	if(end==1){
	    $('#feedback').empty();
	    $('#feedback').append(message);
	    $('#feedback').append("<br><br><a id='replay' class='button'>המשיכו</a>");
	}
	$('#replay').on("click",function (){
		if(questionBank.length>0){
			finalPage()}
		else{finalPage()}
	});
}//victory
		
function defeatMessage(){
	document.activeElement.blur();
	$(document).off("keyup", handleKeyUp);
	$('#feedback').append("You're Dead!<br>(answer= "+ currentWord +")<div id='replay' class='button'>CONTINUE</div>");
	$('#replay').on("click",function (){
		if(questionBank.length>0){
			gameScreen()}
		else{finalPage()}
	});
}//defeat

function finalPage(){
	$('#gameContent').empty();
	$('#gameContent').append('<div id="finalMessage">תודה רבה ששיחקתם יום עצמאות שמח!</div>');
}//finalpage
	
	});//doc ready