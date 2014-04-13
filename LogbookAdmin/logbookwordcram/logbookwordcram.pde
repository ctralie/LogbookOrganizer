import wordcram.*;

//PImage image = loadImage("../mask.gif");
//Shape imageShape = new ImageShaper().shape(image, #000000);
//ShapeBasedPlacer placer = new ShapeBasedPlacer(imageShape);

size(1000, 800);

background(#FFFFFF);

//PFont averia = createFont("AveriaSerif-Regular.ttf", 1);
//PFont janeAusten = createFont("JaneAust.ttf", 1);

new WordCram(this)
  .fromTextFile("../logbookText.txt")
  //.withFonts(averia, janeAusten)
  //.withPlacer(placer)
  //.withNudger(placer)
  .withColors(#B20E0E, #0E12B2)
  .angledAt(0)
  .withWordPadding(1)
  .drawAll();
