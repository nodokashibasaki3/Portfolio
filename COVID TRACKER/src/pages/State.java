package pages;
import java.util.ArrayList;

import processing.core.PApplet;
import processing.core.PImage;
import statistics.StatesGraphics;

/**
 * 
 * @author roopa srinivas
 *
 */
public class State extends Frame{
	private StatesGraphics graph;
	private String name;
	private PImage map, infoGraph;
	private int mapWidth, mapHeight;
	private int screenHeight, screenWidth;
	
	private float buttonDistance;
	private int buttonWidth, buttonHeight;
	private int buttonX, buttonY;
	
	private ArrayList<String> vaccine;
	
	private boolean clickVaxAvailable, clickVaxDistributed, clickDistPercent, clickPeopleVaxed, clickTotalVaxPercent, clickFullyVaxed, clickFullyVaxedPercent;
	private String vaxAvailable, vaxDist, distPercent, peopleVaxed, vaxedPercent, peopleFullyVaxed, fullyVaxedPercent;
	private String vaxAvailableString, vaxDistString, distPercentString, peopleVaxedString, vaxedPercentString, peopleFullyVaxedString, fullyVaxedPercentString;
	private String vaxAvailableDisplay, vaxDistDisplay, distPercentDisplay, peopleVaxedDisplay, vaxedPercentDisplay, peopleFullyVaxedDisplay, fullyVaxedPercentDisplay;
	
	private boolean hasBeenReset;
	
	/**
	 * no-args StatesGraphic constructor
	 */
	public State() {
		super("US_MAP.png");
		graph = new StatesGraphics();
	}
	
	/**
	 * specifies the state for which we are drawing the graphs and obtaining statistics, also sets the picture of the state
	 * @param stateName full name of the state
	 */
	public State(String stateName) {
		super(stateName+".png");
		graph = new StatesGraphics(stateName);
		name = stateName;
		clickVaxAvailable = false;
		clickVaxDistributed = false;
		clickDistPercent = false;
		clickPeopleVaxed = false;
		clickTotalVaxPercent = false;
		clickFullyVaxed = false;
		clickFullyVaxedPercent = false;
		vaxAvailable = " " ;
		vaxDist = " " ;
		distPercent = " " ;
		peopleVaxed = " " ;
		vaxedPercent = " " ;
		peopleFullyVaxed = " " ;
		fullyVaxedPercent = " " ;
		vaxAvailableString = "total vaccinations available";
		vaxDistString = "total vaccinations distributed";
		distPercentString = "total distribution percentage";
		peopleVaxedString = "people vaccinated";
		vaxedPercentString = "total vaccinations percentage";
		peopleFullyVaxedString = "people fully vaccinated";
		fullyVaxedPercentString = "fully vaccinated percentage";
		vaxAvailableDisplay = "" ;
		vaxDistDisplay = "" ;
		distPercentDisplay = "" ;
		peopleVaxedDisplay = "" ;
		vaxedPercentDisplay = "" ;
		peopleFullyVaxedDisplay = "" ;
		fullyVaxedPercentDisplay = "" ;
	}
	
	/**
	 * draws the graph generated from the StatesGraphics class and writes all the numerical statistics
	 * @param surface PApplet that it is being drawn on
	 */
	public void draw(PApplet surface) {
		if (vaccine == null) {
			vaccine = graph.getVaccineInfo();
			if (graph.getInfoAvailable()) {
				vaxAvailable = vaccine.get(2);
				vaxDist = vaccine.get(3);
				distPercent = vaccine.get(9) + "% of the state population";
				peopleVaxed = vaccine.get(4);
				vaxedPercent = vaccine.get(6) + "% of the state population";
				peopleFullyVaxed = vaccine.get(7);
				fullyVaxedPercent = vaccine.get(5) + "% of the state population";
			}
			graph.createGraph(surface, 7*(surface.width/11), surface.height/20, name);
		}
		map = surface.loadImage("maps/" + name +".png");
		
		mapWidth = map.width;
		mapHeight = map.height;
		screenHeight = surface.height;
		screenWidth = surface.width;
		
		
		
		if (screenHeight < screenWidth) {
			map.resize(0, (screenHeight/2-screenHeight/50));
			int heightResizedArea = map.width*map.height;
			map.resize(screenWidth/2, 0);
			int widthResizedArea = map.width*map.height;
			if (heightResizedArea < widthResizedArea) {
				map.resize(0, (screenHeight/2-screenHeight/50));
			}
		} else {
			map.resize(screenWidth/2, 0);
		}
		
		
		

		surface.image(map, screenWidth/100, screenHeight/100);
		
		infoGraph = surface.loadImage("graphs/" + name + ".png");
		surface.image(infoGraph, (float)(7*(screenWidth/11)-(0.4*graph.getGraphWidth())), (float)(screenHeight/20-(0.1*graph.getGraphHeight())));

		drawDropDownButton(surface, screenWidth);
		
		
		
		
		graph.draw(surface);
		
		
		if (clickVaxAvailable) {
			vaxAvailableDisplay = (vaxAvailable);
		} else {
			vaxAvailableDisplay = (vaxAvailableString);
		}
		if (clickVaxDistributed) {
			vaxDistDisplay = vaxDist;
		} else {
			vaxDistDisplay = vaxDistString;
		}
		if (clickDistPercent) {
			distPercentDisplay = distPercent;
		} else {
			distPercentDisplay = distPercentString;
		}
		if (clickPeopleVaxed) {
			peopleVaxedDisplay = peopleVaxed;
		} else {
			peopleVaxedDisplay = peopleVaxedString;
		}
		if (clickTotalVaxPercent) {
			vaxedPercentDisplay = vaxedPercent;
		} else {
			vaxedPercentDisplay = vaxedPercentString;
		}
		if (clickFullyVaxed) {
			peopleFullyVaxedDisplay = peopleFullyVaxed;
		} else {
			peopleFullyVaxedDisplay = peopleFullyVaxedString;
		}
		if (clickFullyVaxedPercent) {
			fullyVaxedPercentDisplay = fullyVaxedPercent;
		} else {
			fullyVaxedPercentDisplay = fullyVaxedPercentString;
		}
		
	}

	/**
	 * resets all the click boolean fields to false
	 */
	public void reset() {
		
		setClickDistPercent(false);
		setClickFullyVaxed(false);
		setClickFullyVaxedPercent(false);
		setClickPeopleVaxed(false);
		setClickTotalVaxPercent(false);
		setClickVaxAvailable(false);
		setClickVaxDistributed(false);
		setHasBeenReset(true);
	}
	
	//get methods
	/**
	 * @return name of the state
	 */
	public String getName() {
		return name;
	}
	
	/**
	 * 
	 * @return graph associated with this state
	 */
	public StatesGraphics getGraph() {
		return graph;
	}
	
	/**
	 * 
	 * @return x coordinate of the button
	 */
	public int getButtonX() {
		return buttonX;
	}
	
	/**
	 * 
	 * @return y coordinate of the button
	 */
	public int getButtonY() {
		return buttonY;
	}
	
	/**
	 * 
	 * @return width of button
	 */
	public int getButtonWidth() {
		return buttonWidth;
	}
	
	/**
	 * 
	 * @return height of button
	 */
	public int getButtonHeight() {
		return buttonHeight;
	}
	
	/**
	 * 
	 * @return distance of one button to another
	 */
	public float getButtonDistance() {
		return buttonDistance;
	}
	
	/**
	 * 
	 * @return state of clickVaxAvailable field
	 */
	public boolean getClickVaxAvailable() {
		return clickVaxAvailable;
	}
	
	/**
	 * 
	 * @return state of clickVaxDistributed field
	 */
	public boolean getClickVaxDistributed() {
		return clickVaxDistributed;
	}
	
	/**
	 * 
	 * @return state of clickDistPercent field
	 */
	public boolean getClickDistPercent() {
		return clickDistPercent;
	}
	
	/**
	 * 
	 * @return state of clickPeopleVaxed field
	 */
	public boolean getClickPeopleVaxed() {
		return clickPeopleVaxed;
	}
	
	/**
	 * 
	 * @return state of clickTotalVaxPercent field
	 */
	public boolean getClickTotalVaxPercent() {
		return clickTotalVaxPercent;
	}
	
	/**
	 * 
	 * @return state of clickFullyVaxed field
	 */
	public boolean getClickFullyVaxed() {
		return clickFullyVaxed;
	}
	
	/**
	 * 
	 * @return state of clickFullyVaxedPercent field
	 */
	public boolean getClickFullyVaxedPercent() {
		return clickFullyVaxedPercent;
	}
	
	/**
	 * 
	 * @return actual statistics for vaxAvailable
	 */
	public String getVaxAvailable() {
		return vaxAvailable;
	}
	
	/**
	 * 
	 * @return text that is displayed on the vaxAvailable button
	 */
	public String getVaxAvailableDisplay() {
		return vaxAvailableDisplay;
	}
	
	/**
	 * 
	 * @return default text on vaxAvailable button
	 */
	public String getVaxAvailableString() {
		return vaxAvailableString;
	}
	
	/**
	 * 
	 * @return actual statistics for vaxDist
	 */
	public String getVaxDist() {
		return vaxDist;
	}
	
	/**
	 * 
	 * @return text that is displayed on the vaxDist button
	 */
	public String getVaxDistDisplay() {
		return vaxDistDisplay;
	}
	
	/**
	 * 
	 * @return default text on vaxDist button
	 */
	public String getVaxDistString() {
		return vaxDistString;
	}
	
	/**
	 * 
	 * @return actual statistics for distPercent
	 */
	public String getDistPercent() {
		return distPercent;
	}
	
	/**
	 * 
	 * @return text that is displayed on the distPercent button
	 */
	public String getDistPercentDisplay() {
		return distPercentDisplay;
	}
	
	/**
	 * 
	 * @return default text on distPercent button
	 */
	public String getDistPercentString() {
		return distPercentString;
	}
	
	/**
	 * 
	 * @return actual statistics for peopleVaxed
	 */
	public String getPeopleVaxed() {
		return peopleVaxed;
	}
	
	/**
	 * 
	 * @return text that is displayed on the peopleVaxed button
	 */
	public String getPeopleVaxedDisplay() {
		return peopleVaxedDisplay;
	}
	
	/**
	 * 
	 * @return default text on peopleVaxed button
	 */
	public String getPeopleVaxedString() {
		return peopleVaxedString;
	}
	
	/**
	 * 
	 * @return actual statistics for vaxedPercent
	 */
	public String getVaxedPercent() {
		return vaxedPercent;
	}
	
	/**
	 * 
	 * @return text that is displayed on the vaxedPercent button
	 */
	public String getVaxedPercentDisplay() {
		return vaxedPercentDisplay;
	}
	
	/**
	 * 
	 * @return default text on vaxedPercent button
	 */
	public String getVaxedPercentString() {
		return vaxedPercentString;
	}
	
	/**
	 * 
	 * @return actual statistics for peopleFullyVaxed
	 */
	public String getPeopleFullyVaxed() {
		return peopleFullyVaxed;
	}
	
	/**
	 * 
	 * @return text that is displayed on the peopleFullyVaxed button
	 */
	public String getPeopleFullyVaxedDisplay() {
		return peopleFullyVaxedDisplay;
	}
	
	/**
	 * 
	 * @return default text on peopleFullyVaxed button
	 */
	public String getPeopleFullyVaxedString() {
		return peopleFullyVaxedString;
	}
	
	/**
	 * 
	 * @return actual statistics for fullyVaxedPercent
	 */
	public String getFullyVaxedPercent() {
		return fullyVaxedPercent;
	}
	
	/**
	 * 
	 * @return text that is displayed on the fullyVaxedPercent button
	 */
	public String getFullyVaxedPercentDisplay() {
		return fullyVaxedPercentDisplay;
	}
	
	/**
	 * 
	 * @return default text on fullyVaxedPercent button
	 */
	public String getFullyVaxedPercentString() {
		return fullyVaxedPercentString;
	}
	
	/**
	 * 
	 * @return state of hasBeenReset field
	 */
	public boolean getHasBeenReset() {
		return hasBeenReset;
	}
	
	//set methods

	/**
	 * sets buttonX to num
	 * @param num new x coordinate
	 */
	public void setButtonX(int num) {
		buttonX = num;
	}
	
	/**
	 * sets buttonY to num
	 * @param num new y coordinate
	 */
	public void setButtonY(int num) {
		buttonY = num;
	}
	
	/**
	 * sets buttonWidth to num
	 * @param num new button width
	 */
	public void setButtonWidth(int num) {
		buttonWidth = num;
	}
	
	/**
	 * sets buttonHeight to num
	 * @param num new button height
	 */
	public void setButtonHeight(int num) {
		buttonHeight = num;
	}
	
	/**
	 * sets buttonDistance to num
	 * @param num new button distance
	 */
	public void setButtonDist(float num) {
		buttonDistance = num;
	}
	
	/**
	 * sets clickVaxAvailable to state
	 * @param state (true or false)
	 */
	public void setClickVaxAvailable(boolean state) {
		clickVaxAvailable = (state);
	}
	
	/**
	 * sets clickVaxDistributed to state
	 * @param state (true or false)
	 */
	public void setClickVaxDistributed(boolean state) {
		clickVaxDistributed = (state);
	}
	
	/**
	 * sets clickDistPercent to state
	 * @param state (true or false)
	 */
	public void setClickDistPercent(boolean state) {
		clickDistPercent = (state);
	}
	
	/**
	 * sets clickPeopleVaxed to state
	 * @param state (true or false)
	 */
	public void setClickPeopleVaxed(boolean state) {
		clickPeopleVaxed = (state);
	}
	
	/**
	 * sets clickTotalVaxPercent to state
	 * @param state (true or false)
	 */
	public void setClickTotalVaxPercent(boolean state) {
		clickTotalVaxPercent = (state);
	}
	
	/**
	 * sets clickFullyVaxed to state
	 * @param state (true or false)
	 */
	public void setClickFullyVaxed(boolean state) {
		clickFullyVaxed = (state);
	}
	
	/**
	 * sets clickFullyVaxedPercent to state
	 * @param state (true or false)
	 */
	public void setClickFullyVaxedPercent(boolean state) {
		clickFullyVaxedPercent = (state);
	}
	
	/**
	 * sets vaxAvailableDisplay to txt
	 * @param txt new display text
	 */
	public void setVaxAvailableDisplay(String txt) {
		vaxAvailableDisplay = txt;
	}
	
	/**
	 * sets vaxDistDisplay to txt
	 * @param txt new display text
	 */
	public void setVaxDistDisplay(String txt) {
		vaxDistDisplay = txt;
	}
	
	/**
	 * sets distPercentDisplay to txt
	 * @param txt new display text
	 */
	public void setDistPercentDisplay(String txt) {
		distPercentDisplay = txt;
	}
	
	/**
	 * sets peopleVaxedDisplay to txt
	 * @param txt new display text
	 */
	public void setPeopleVaxedDisplay(String txt) {
		peopleVaxedDisplay = txt;
	}
	
	/**
	 * sets vaxedPercentDisplay to txt
	 * @param txt new display text
	 */
	public void setVaxedPercentDisplay(String txt) {
		vaxedPercentDisplay = txt;
	}
	
	/** 
	 * sets peopleFullyVaxedDisplay to txt
	 * @param txt new display text
	 */
	public void setPeopleFullyVaxedDisplay(String txt) {
		peopleFullyVaxedDisplay = txt;
	}
	
	/**
	 * sets fullyVaxedPercentDisplay to txt
	 * @param txt new display text
	 */
	public void setFullyVaxedPercentDisplay(String txt) {
		fullyVaxedPercentDisplay = txt;
	}
	
	/**
	 * sets hasBeenReset to state
	 * @param state (true or false)
	 */
	public void setHasBeenReset(boolean state) {
		hasBeenReset = state;
	}
}
