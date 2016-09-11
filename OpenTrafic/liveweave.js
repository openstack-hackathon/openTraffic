
var svg = d3.select("body")
   .append("svg")
   .attr("width", 600)
   .attr("height", 600);

var positionDistance = 25; //Pixeles to move
var carX;
var actualPositionCarX=0;
var carY;
var actualPositionCarY=0;

$('#createX').on('click',function(){carX = createCarX();});
$('#createY').on('click',function(){carY = createCarY();});

$('#moveX').on('click',function(){moveCarX(1000,actualPositionCarX+positionDistance);});
$('#moveY').on('click',function(){moveCarY(1000,actualPositionCarY+positionDistance);});

function createCarX(){
  var car = svg.append("rect")
  .attr("x",300)
  .attr("y",0)
  .attr("width",10)
  .attr("height",20)
  .style("fill","red");
  
  return car;
}

function moveCarX(vel,pos){
  carX
  .transition()  
  .duration(vel)
  .attr("y",pos);
  
  actualPositionCarX=pos;
}


function createCarY(){

var car = svg.append("rect")
  .attr("x",0)
  .attr("y",300)
  .attr("width",20)
  .attr("height",10)
  .style("fill","blue");
  
  return car;
}

function moveCarY(vel,pos){
  carY
  .transition()  
  .duration(vel)
  .attr("x",pos);
  
  actualPositionCarY=pos;
}