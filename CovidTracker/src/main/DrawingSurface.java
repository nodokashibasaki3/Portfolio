package main;

import pages.Country;
import pages.MoreInfo;
import pages.State;
import processing.core.PApplet;
import processing.core.PFont;
import statistics.StatesGraphics;

/**draws the graphics and
 * 
 * @author sophie lin
 */
public class DrawingSurface extends PApplet{
	private PFont titles, body;
	
	private Country map;
	private MoreInfo moreInfo;
	private int animation=0;
	
	private int buttonW, buttonH;
	private int mapX, mapY;   	 //coordinates and width/height  of the map button
	private boolean mapClicked;		//if map button has been clicked
	
	private int infoX, infoY;   //coordinates and width/height  of the map button
	private boolean infoClicked;		//if INFO button has been clicked
	
	private int insX, insY;    //coordinates and width/height  of the map button
	private boolean insClicked;		//if map button has been clicked
	
	private int backButtonWidth, backButtonHeight;
	private int backButtonX, backButtonY;
	private int quitX, quitY;
	private int backButtonTextSize;
	private int r, g, b, r1, g1, b1;
	private boolean mainPage;
	private boolean mapPage;
	private boolean infoPage;
	private boolean insPage;
	public boolean quit;
	private int x;
	
	/**
	 * no-args constructor initializes fields
	 */
	public DrawingSurface() {
		map = new Country();
		moreInfo = new MoreInfo();
		mainPage = true;
		mapPage = false;
		infoPage = false;
		mapClicked = false;
		infoClicked = false;
		insClicked = false;
		quit = false;
		  r = 255;
		  g = 202;
		  b = 240;
		  r1= 255;
		  g1= 237;
		  b1= 251;
		  x = 0;
	}
	/**
	 * makes the window full screen
	 */
	public void settings() {
		fullScreen();
	}
	/**
	 * sets up the window
	 */
	public void setup() {
		titles = createFont("fonts/LondrinaOutline-Regular.ttf", 10);
		body = createFont("fonts/Montserrat-Regular.ttf", 10);
		textSize(width/60);
		fill(252);
		textSize(12);
	}
	
	/*
	 * draws all aspects of the project
	 */
	public void draw() {
		background(255);
		textSize(width/60);
		fill(252);
		  //update fields
		buttonW= width/3;
		buttonH = height/10;
		insX = width/3;
		insY = 3*(int)(height/10.0);
		mapX = width/3;
		mapY = 5*(int)(height/10.0);
		infoX = width/3;
		infoY = 7*(int)(height/10.0);
		backButtonWidth = width/25;
		backButtonHeight = height/25;
		quitX = width-backButtonWidth-width/50;
		quitY = height-backButtonHeight-height/100;
		backButtonX = width-backButtonWidth-2*width/25;
		backButtonY = height-backButtonHeight-height/100;
		backButtonTextSize = height/50;
		
		  //checks what page the window is on
		  if(mainPage) {
			  r = 255;
			  g = 202;
			  b = 240;
			  r1= 255;
			  g1= 237;
			  b1= 251;
			  fill(255);
			  rect(0, 0, width, height);
			  fill(0);
			  callFont(titles, 0);
			  textSize(width/18);
				text("Covid Vaccine Tracker", width/2, height/10);
				textSize(width/60);
			  buttons();
			  if(mapClicked) {
				  mapPage = true;
				  mainPage = false;
				  infoPage = false;
				  insPage = false;
			  }
			  if(infoClicked) {
				  mapPage = false;
				  mainPage = false;
				  infoPage = true;
				  insPage = false;
		  	}
			  if(insClicked) {
				  mapPage = false;
				  mainPage = false;
				  infoPage = false;
				  insPage = true;
			  }
		  }
		  if(mapPage) {
			  if(x<75) {
				  fill(0);
				  callFont(titles, 0);
				  textSize(width/18);
				  text("Covid Vaccine Tracker", width/2, height/10);
				  textSize(width/60);
				  callFont(body, 0);
				  fill(252);
				  animation("going to map", mapX, mapY, buttonW, buttonH);
				  fill(r1, g1, b1);
				  	drawButton(infoX, infoY, buttonW, buttonH, "more information");
				  	drawButton(insX, insY, buttonW, buttonH, "instructions");
				  x++;
			  }
			  else {
				  r1 = 255;
				  g1 = 255;
				  b1 = 230;
				  r= 255;
				  g= 255;
				  b= 168;
			  
				  goToMap();
			  }
		  }
		  if(infoPage) {
			  if(x<75) {
				  fill(0);
				  callFont(titles, 0);
				  textSize(width/18);
				  text("Covid Vaccine Tracker", width/2, height/10);
				  textSize(width/60);
				  callFont(body, 0);
				  fill(252);
				  animation("going to more information", infoX, infoY, buttonW, buttonH);
				  fill(r1, g1, b1);
				  	drawButton(mapX, mapY, buttonW, buttonH, "map");
				  	drawButton(insX, insY, buttonW, buttonH, "instructions");
				  x++;
			  }
			  else {
				  r = 221;
				  g = 200;
				  b = 255;
				  r1= 243;
				  g1= 232;
				  b1= 255;
			  
				  goToInfo();
			  }
		  }
		  if(insPage) {
			  if(x<75) {
				  fill(0);
				  callFont(titles, 0);
				  textSize(width/18);
				  text("Covid Vaccine Tracker", width/2, height/10);
				  callFont(body, 0);
				  textSize(width/60);
				  fill(252);
				  animation("going to instructions", insX, insY, buttonW, buttonH);
				  fill(r1, g1, b1);
				  drawButton(mapX, mapY, buttonW, buttonH, "map");
				  drawButton(infoX, infoY, buttonW, buttonH, "more information");
				  x++;
			  }
			  else
				  goToIns();
		  }
		  textSize(backButtonTextSize);
		  if(overButton(quitX, quitY, backButtonWidth, backButtonHeight)) 
			  fill(r, g, b);
			else {
				fill(r1,g1,b1);
			}
		  drawButton(quitX, quitY, backButtonWidth, backButtonHeight, "quit");
		  textSize(width/60);
		  if(quit) {
			  exit();
		  }
		
	}
	/**checks if the mouse is over the button
	 * 
	 * @param x x coordinate of the button
	 * @param y y coordinate of the button
	 * @param w width of the button
	 * @param h height of the button
	 * @return boolean if the mouse is over the button
	 */
	public boolean overButton(int x, int y, int w, int h) {
		    if (mouseX > x && mouseX < (x + w) && mouseY > y && mouseY < (y + h)) {
		      return true;
		    }
		    return false;
		  }
	/**detects if the mouse is clicked
	 * and changes booleans to change pages
	 */
	public void mouseClicked() {
		if(mainPage) {
			if (overButton(mapX, mapY, buttonW, buttonH)) {
				mapClicked = true;
				infoClicked = false;
				insClicked = false;
				x=0;
			} 
			if (overButton(infoX, infoY, buttonW, buttonH)) {
				infoClicked = true;
				mapClicked = false;
				insClicked = false;
				x= 0;
		  } 
			if (overButton(insX, insY, buttonW, buttonH)) {
				insClicked = true;
				mapClicked = false;
				infoClicked = false;
				x= 0;
		  } 
		}
		if(mapPage) {
			map.setOpenDropDown(overButton(map.getScreenW()-45, 0, 45, 40));
			if(overButton(backButtonX, backButtonY, backButtonWidth, backButtonHeight)) {
				mapPage = false;
				mainPage = true;
				reset();
			}
			if(!map.getStatePageOpen()) {
				if(overButton((int)(map.getButtonX()),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight())) {
					map.setClickVaxName(!map.getClickVaxName());
				}
				if(overButton((int)(map.getButtonX()+map.getButtonDistance()), (int)(map.getButtonY()+ map.getButtonDistance() /3), map.getButtonWidth(), map.getButtonHeight())) {
					map.setClickAvailableVax(!map.getClickAvailableVax());
				}
				if(overButton((int)(map.getButtonX()+map.getButtonDistance()*2), (int)(map.getButtonY()+ map.getButtonDistance() /3), map.getButtonWidth(), map.getButtonHeight())) {
					map.setClickPeopleVaxed(!map.getClickPeopleVaxed()); 
				}
				if(overButton((int)(map.getButtonX()+map.getButtonDistance()*3), (int)(map.getButtonY()+ map.getButtonDistance() /3), map.getButtonWidth(), map.getButtonHeight())) {
					map.setClickFullyVaxed(!map.getClickFullyVaxed());
				}
			}	else { 
				
				State state = map.getStates().get(map.getStateInput());
				setStateButtonInfo(state);
				
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()), state.getButtonWidth(),state.getButtonHeight())) {
					map.getStates().get(map.getStateInput()).setClickVaxAvailable(!map.getStates().get(map.getStateInput()).getClickVaxAvailable());
				}
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*2), state.getButtonWidth(),state.getButtonHeight())) {
					map.getStates().get(map.getStateInput()).setClickVaxDistributed(!map.getStates().get(map.getStateInput()).getClickVaxDistributed());
				}
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*3), state.getButtonWidth(),state.getButtonHeight())) {
					map.getStates().get(map.getStateInput()).setClickDistPercent(!map.getStates().get(map.getStateInput()).getClickDistPercent());
				}
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*4), state.getButtonWidth(),state.getButtonHeight())) {
					map.getStates().get(map.getStateInput()).setClickPeopleVaxed(!map.getStates().get(map.getStateInput()).getClickPeopleVaxed());
				}
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*5), state.getButtonWidth(),state.getButtonHeight())) {
					map.getStates().get(map.getStateInput()).setClickTotalVaxPercent(!map.getStates().get(map.getStateInput()).getClickTotalVaxPercent());
				} 
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*6), state.getButtonWidth(),state.getButtonHeight())) {
					map.getStates().get(map.getStateInput()).setClickFullyVaxed(!map.getStates().get(map.getStateInput()).getClickFullyVaxed());
				}
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*7), state.getButtonWidth(),state.getButtonHeight())) {
					map.getStates().get(map.getStateInput()).setClickFullyVaxedPercent(!map.getStates().get(map.getStateInput()).getClickFullyVaxedPercent());
				}
			}
		}
		if(infoPage) {
			if(overButton(backButtonX, backButtonY, backButtonWidth, backButtonHeight)) {
				infoPage = false;
				mainPage = true;
				reset();
			}
			if(overButton((int)(moreInfo.getButtonX()-width/3.5), (int)moreInfo.getButtonY(), moreInfo.getButtonWidth(), moreInfo.getButtonHeight())) {
				moreInfo.setPfizer(true);
				moreInfo.setJohnson(false);
				moreInfo.setModerna(false);
			}
			if(overButton((int)(2*moreInfo.getButtonX()-width/3.5),(int)moreInfo.getButtonY(), moreInfo.getButtonWidth(), moreInfo.getButtonHeight())) {
				moreInfo.setPfizer(false);
				moreInfo.setJohnson(true);
				moreInfo.setModerna(false);
			}
			if(overButton((int)(3*moreInfo.getButtonX()-width/3.5), (int)(moreInfo.getButtonY()), moreInfo.getButtonWidth(), moreInfo.getButtonHeight())) {
				moreInfo.setPfizer(false);
				moreInfo.setJohnson(false);
				moreInfo.setModerna(true);
			}
		}
		if(insPage) {
			if(overButton(backButtonX, backButtonY, backButtonWidth, backButtonHeight)) {
				insPage = false;
				mainPage = true;
				reset();
			}
		}
		 if(overButton(quitX, quitY, backButtonWidth, backButtonHeight)) 
			 quit = true;
	}
	/**
	 * draws the animation for the buttons
	 * @param text text of what the animation is going to look like
	 * @param x x coordinate of the button
	 * @param y y coordinate of the button
	 * @param w width of the butotn
	 * @param h height of the button]
	 * @post fill(252)
	 */
	private void animation(String text, int x, int y, int w, int h) {
		callFont(body, 0);
		textSize(width/60);
		 fill(r, g, b);
		  rect(x, y, w, h, 10);
		  fill(0, 102, 153);
		  if(animation<=25) 
			  text(text+ ".",x+ (w / 2), y + (h / 2));
		  else if(animation>25 && animation<=50) {
			  text(text+ "..",x + (w / 2), y + (h / 2));
		  }
		  else if(animation>50 && animation<=75) 
			  text(text+ "...", x + (w / 2), y + (h / 2));
		  else
			  animation = 0;
   	 	animation++;
   	 	fill(r1, g1, b1);
	}
	/**checks if the mouse is over the map and info button
	 * makes the button darker when you hover over it and draws the button
	 * @post fill
	 */
	public void buttons() {
		callFont(body, 0);
		textSize(width/60);
		if(overButton(mapX, mapY, buttonW,buttonH)) 
			fill(r, g, b);
		else {
			fill(r1,g1,b1);
			}
	    drawButton(mapX, mapY, buttonW, buttonH, "map");
	
	    if(overButton(infoX, infoY, buttonW, buttonH)) 
	    	fill(r, g, b);
		else {
			fill(r1,g1,b1);
			}
	    drawButton(infoX, infoY, buttonW, buttonH, "more information");
	    if(overButton(insX, insY, buttonW, buttonH)) 
	    	fill(r, g, b);
		else {
			fill(r1,g1,b1);
			}
		 drawButton(insX, insY, buttonW, buttonH, "instructions");
	    
	}
	/**
	 * draws a button 
	 * @param x x coordinate of the button
	 * @param y y coordinate of the button
	 * @param w width of the button
	 * @param h height of the button
	 * @param text text on the button
	 */
	public void drawButton(int x, int y, int w, int h, String text) {
		rect(x, y, w, h, 10);
    	textAlign(CENTER, CENTER);
    	fill(0);
    	text(text, x + w/2, y + h/2);
    	fill(r1, g1, b1);
	}
	/**resets all the variables to default so when someone decides to go back, it will be all default
	 * 
	 */
	public void reset() {
		animation=0;
		mapClicked = false;
		infoClicked= false;
		insClicked = false;
		moreInfo.setPfizer(false);
		moreInfo.setJohnson(false);
		moreInfo.setModerna(false);
		map.setStatePageOpen(false);
		map.setClickAvailableVax(false);
		map.setClickFullyVaxed(false);
		map.setClickPeopleVaxed(false);
		map.setClickVaxName(false);
		x = 0;
		r = 255;
		g = 202;
		b = 240;
		r1= 255;
		g1= 237;
		b1= 251;
	}
	/**goes to map page
	 * draws a back button
	 * @post fill(255)
	 */
	public void goToMap() {
		fill(255);
		rect(0, 0, width, height);
		map.draw(this);
		if(map.getStatePageOpen()) {
			r = 99;
			g = 207;
			b = 248;
			r1= 214;
			g1= 244;
			b1= 255;
			State state = map.getStates().get(map.getStateInput());
			if (state.getGraph().getInfoAvailable()) {
				state.setButtonDist(height/20);
				state.setButtonHeight(height/25);
				state.setButtonWidth(width/3);
				state.setButtonX(width/20);
				state.setButtonY(height* 11 /20);
				setStateButtonInfo(state);
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()), state.getButtonWidth(),state.getButtonHeight())) {
					fill(r, g, b);
				}
					else 
						fill(r1,g1,b1);
				drawButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()), state.getButtonWidth(),state.getButtonHeight(), state.getVaxAvailableDisplay());
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*2), state.getButtonWidth(),state.getButtonHeight())) 
					fill(r, g, b);
					else 
						fill(r1,g1,b1);
				drawButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*2), state.getButtonWidth(),state.getButtonHeight(), state.getVaxDistDisplay());
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*3), state.getButtonWidth(),state.getButtonHeight())) 
						fill(r, g, b);
					else 
						fill(r1,g1,b1);
				drawButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*3), state.getButtonWidth(),state.getButtonHeight(), state.getDistPercentDisplay());
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*4), state.getButtonWidth(),state.getButtonHeight())) 
						fill(r, g, b);
					else 
						fill(r1,g1,b1);
				drawButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*4), state.getButtonWidth(),state.getButtonHeight(), state.getPeopleVaxedDisplay());
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*5), state.getButtonWidth(),state.getButtonHeight())) 
						fill(r, g, b);
					else 
						fill(r1,g1,b1);
				drawButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*5), state.getButtonWidth(),state.getButtonHeight(), state.getVaxedPercentDisplay());
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*6), state.getButtonWidth(),state.getButtonHeight())) 
						fill(r, g, b);
					else 
						fill(r1,g1,b1);
				drawButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*6), state.getButtonWidth(),state.getButtonHeight(), state.getPeopleFullyVaxedDisplay());
				if(overButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*7), state.getButtonWidth(),state.getButtonHeight())) 
						fill(r, g, b);
					else 
						fill(r1,g1,b1);
				drawButton(state.getButtonX(), (int)(state.getButtonY()+state.getButtonDistance()*7), state.getButtonWidth(),state.getButtonHeight(), state.getFullyVaxedPercentDisplay());
				
			} else {

			}
			
			
			
		} else {
			if(overButton(map.getButtonX(),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight())) {
	    		fill(r, g, b);
	    	}
	    		
			else {
				fill(r1,g1,b1);
				}
	    	drawButton(map.getButtonX(),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight(), map.getVaxNames());
	    	
	    	if(overButton((int)(map.getButtonX()+map.getButtonDistance()),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight())) 
	    		fill(r, g, b);
			else {
				fill(r1,g1,b1);
				}
	    	drawButton((int)(map.getButtonX()+map.getButtonDistance()),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight(), map.getVaxAvailable());
	    	if(overButton((int)(map.getButtonX()+map.getButtonDistance()*2),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight())) 
	    		fill(r, g, b);
			else {
				fill(r1,g1,b1);
				}
	    	drawButton((int)(map.getButtonX()+map.getButtonDistance()*2),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight(), map.getPeopleVaxed());
	    	if(overButton((int)(map.getButtonX()+map.getButtonDistance()*3),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight())) 
	    		fill(r, g, b);
			else {
				fill(r1,g1,b1);
				}
	    	drawButton((int)(map.getButtonX()+map.getButtonDistance()*3),(int)(map.getButtonY()+ map.getButtonDistance()/3), map.getButtonWidth(), map.getButtonHeight(), map.getPeopleFullyVaxed());
		}
	
		fillBackButton();
	}
	/**
	 * goes to info page 
	 * also makes the buttons dark when hovering over it
	 * draws a back button
	 * @post fill
	 */
	public void goToInfo() {
		callFont(body, 0);
		fill(255);
		rect(0, 0, width, height);
		moreInfo.draw(this);
		fillBackButton();
		textSize(height/50);
    	if(overButton((int)(moreInfo.getButtonX()-width/3.5), (int)moreInfo.getButtonY(), moreInfo.getButtonWidth(), moreInfo.getButtonHeight())) {
    		fill(r, g, b);
    	}else {
    			fill(r1,g1,b1);
    			}
    	drawButton((int) (moreInfo.getButtonX()-width/3.5), (int)moreInfo.getButtonY(), moreInfo.getButtonWidth(),moreInfo.getButtonHeight(), "Pfizer-BioNTech");
	
		if(overButton((int)(2*moreInfo.getButtonX()-width/3.5), (int)(moreInfo.getButtonY()), moreInfo.getButtonWidth(), moreInfo.getButtonHeight())) {
			fill(r, g, b);
		}else {
				fill(r1,g1,b1);
				}
			drawButton( (int)(2*moreInfo.getButtonX()-width/3.5), (int)(moreInfo.getButtonY()), moreInfo.getButtonWidth(),moreInfo.getButtonHeight(), "Johnson & Johnson");
		
		if(overButton((int)(3*moreInfo.getButtonX()-width/3.5), (int)(moreInfo.getButtonY()), moreInfo.getButtonWidth(), moreInfo.getButtonHeight())) {
			fill(r, g, b);
		}else {
			fill(r1,g1,b1);
			}
		drawButton( (int)(3*moreInfo.getButtonX()-width/3.5),  (int)(moreInfo.getButtonY()), moreInfo.getButtonWidth(),moreInfo.getButtonHeight(), "Moderna");
		
	}
	/**
	 * goes to instruction page
	 * @post fill(0)
	 * @post text Size
	 * @post leftAlign
	 */
	public void goToIns() {
		callFont(titles, 0);
		fill(255);
		rect(0, 0, width, height);
		fill(0);
		textSize(width/27);
		text("Instructions", width/2, height/10);
		callFont(body, 0);
		textSize(width/60);
		textAlign(LEFT);
		
		text("- press the map button to go to the country map\n"
				+ "- the country map page shows a map of the country with buttons that will reveal \n   countrywide statistics about the vaccines when they are clicked on\n"
				+ "- click each button to show the information"
				+ "- on the map page, click the three lines in the corner to open \n   a drop down\n"
				+ "- from there, there is an option to choose a state, which leads to the map of that state with its \n   corresponding statistics that will be revealed when the button is clicked on\n\n"
				+ "- press the more info button to get more information\n"
				+ "- the more information page will give you more information about the different types of vaccine\n\n"
				+ "- press the back button to go back to the main page\n"
				+ "- press the quit button to exit the program", 2*width/25, 3*height/10);
	    	fillBackButton();
	    	
	}
	/**
	 *  makes the font 
	 *  @post fontColor
	 *  @post font 
	 **/
	private void callFont(PFont font, int fontColor) {
		fill(fontColor);
		textFont(font);
	}
	/**
	 * fills and draws the back button
	 * @post fill
	 * @post textSize
	 */
	public void fillBackButton() {
		if(overButton(backButtonX, backButtonY, backButtonWidth, backButtonHeight)) 
			fill(r, g, b);
		else {
			fill(r1,g1,b1);
			}
		textSize(backButtonTextSize);	
		drawButton(backButtonX, backButtonY, backButtonWidth, backButtonHeight, "back");
	}
	/**
	 * set the state buttons info
	 * @param state State
	 */
	public void setStateButtonInfo(State state) {
		if (state.getClickVaxAvailable()) {
			state.setVaxAvailableDisplay(state.getVaxAvailable());
		} else {
			state.setVaxAvailableDisplay(state.getVaxAvailableString());
		}
		if (state.getClickVaxDistributed()) {
			state.setVaxDistDisplay(state.getVaxDist());
		} else {
			state.setVaxDistDisplay(state.getVaxDistString());
		}
		if (state.getClickDistPercent()) {
			state.setDistPercentDisplay(state.getDistPercent());
		} else {
			state.setDistPercentDisplay(state.getDistPercentString());
		}
		if (state.getClickPeopleVaxed()) {
			state.setPeopleVaxedDisplay(state.getPeopleVaxed());
		} else {
			state.setPeopleVaxedDisplay(state.getPeopleVaxedString());
		}
		if (state.getClickTotalVaxPercent()) {
			state.setVaxedPercentDisplay(state.getVaxedPercent());
		} else {
			state.setVaxedPercentDisplay(state.getVaxedPercentString());
		}
		if (state.getClickFullyVaxed()) {
			state.setPeopleFullyVaxedDisplay(state.getPeopleFullyVaxed());
		} else {
			state.setPeopleFullyVaxedDisplay(state.getPeopleFullyVaxedString());
		}
		if (state.getClickFullyVaxedPercent()) {
			state.setFullyVaxedPercentDisplay(state.getFullyVaxedPercent());
		} else {
			state.setFullyVaxedPercentDisplay(state.getFullyVaxedPercentString());
		}
	}


}
