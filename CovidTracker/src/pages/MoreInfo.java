package pages;
import java.awt.Desktop;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;

import processing.core.PApplet;

/**
 * 
 * @author roopa srinivas
 *
 */
public class MoreInfo{
	
	private float buttonX, buttonY;
	private int buttonWidth, buttonHeight;
	private boolean pfizerButton, johnsonButton, modernaButton;
	private int screenHeight, screenWidth;
	
	/**
	 * 
	 * @param surface papplet parameter
	 * @param x x coordinate of button
	 * @param y y coordinate of button
	 * @param w width of button
	 * @param h height of button
	 * @param text text to be displayed inside button
	 */
	public void drawButton(PApplet surface, int x, int y, int w, int h, String text) {
		surface.rect(x, y, w, h, 10);
    	surface.textAlign(surface.CENTER, surface.CENTER);
    	surface.fill(0);
    	surface.text(text, x + w/2, y + h/2);
    	surface.noFill();
	}
	
	/**
	 * draws all aspects of moreInfo class
	 * @param surface papplet parameter
	 */
	public void draw(PApplet surface) {
		screenHeight = surface.height;
		screenWidth = surface.width;
		buttonWidth = screenWidth/4;
		buttonHeight = screenHeight/12;
		drawVaccineButtons(surface);
		drawInfo(surface, screenHeight/50);
		if (pfizerButton) {
			URL url;
			try {
				url = new URL("https://www.cdc.gov/coronavirus/2019-ncov/vaccines/different-vaccines/Pfizer-BioNTech.html");
				openWebpage(url);
				pfizerButton = false;
			} catch (MalformedURLException e) {
				e.printStackTrace();
			}	
		} if (johnsonButton) {
			URL url;
			try {
				url = new URL("https://www.cdc.gov/coronavirus/2019-ncov/vaccines/different-vaccines/janssen.html");
				openWebpage(url);
				johnsonButton = false;
			} catch (MalformedURLException e) {
				e.printStackTrace();
			}	
		} if (modernaButton) {
			URL url;
			try {
				url = new URL("https://www.cdc.gov/coronavirus/2019-ncov/vaccines/different-vaccines/Moderna.html");
				openWebpage(url);
				modernaButton = false;
			} catch (MalformedURLException e) {
				e.printStackTrace();
			}	
		}
	}
	
	/**
	 * draws the vaccine buttons
	 * @param surface papplet parameter
	 * @post textSize screen height/50
	 */
	private void drawVaccineButtons(PApplet surface) {
		buttonX = surface.width/3;
		buttonY = 4*surface.height/5;
		surface.textSize(screenHeight/50);
		drawButton(surface, (int)(buttonX-surface.width/3.5), (int)buttonY, (int)buttonWidth, (int)buttonHeight, "Pfizer-BioNTech");
		drawButton(surface, (int)(2*buttonX-surface.width/3.5), (int)(buttonY), (int)buttonWidth, (int)buttonHeight, "Johnson & Johnson");
		drawButton(surface, (int)(3*buttonX-surface.width/3.5), (int)(buttonY), (int)buttonWidth, (int)buttonHeight, "Moderna");
	}
	
	/**
	 * draws the actual info
	 * @param surface papplet parameter
	 * @post textSize screenHeight/50
	 * @post textAlign left
	 */
	private void drawInfo(PApplet surface, float leading) {
		int startY = screenHeight/10;
		int startX1 = screenWidth/13;
		int startX2 = 7*screenWidth/13;
		int yDifference = screenHeight/30;
		float textSize1 = screenHeight/25;
		float textSize2 = screenHeight/40;
		float textSize3 = screenHeight/65;
		
		surface.textSize(textSize1);
		surface.text("ALL INFO GATHERED DIRECTLY FROM CDC WEBSITE (as of 05/15/2021)", screenWidth/2, screenHeight/20);
		surface.textAlign(surface.LEFT);
		surface.textLeading(leading);
		surface.textSize(textSize2);
		surface.text("eligibility: ", startX1, startY+(yDifference));
		surface.textSize(textSize3);
		surface.text("     - 12 and older (in all vaccination sites) (only for Pfizer-BioNTech) ", startX1, startY+(yDifference*2));
		surface.textSize(textSize2);
		surface.text("types: ", startX1, startY+(yDifference*4));
		surface.textSize(textSize3);
		surface.text("     - Pfizer-BioNTech (must take 2 shots for full effectiveness) " + "\n" + 
				     "     - Johnson & Johnson (must take 1 shot for full effectiveness)" + "\n" +
				     "     - Moderna (must take 2 shots for full effectiveness)" + "\n" + 
				     "     *use buttons below for more information*", startX1, startY+(yDifference*5));
		surface.textSize(textSize2);
		surface.text("potential side effects: ", startX1, startY+(yDifference*9));
		surface.textSize(textSize3);
		surface.text("     - on arm where you got the shot: pain, redness, swelling" + "\n" + 
					 "     - throughout body: tiredness, headache, muscle pain, chils, fever, nausea" + "\n" + 
					 "     - to reduce discomfort where you got the shot: apply clean, cool, wet washcloth over the area, " + "\n" + 
					 "       use or exercise your arm " + "\n" +
					 "     - to reduce discomfort throughout your whole body: drink lots of fluids, dress lightly " + "\n" + 
					 "     - side effects of second shot is typically more intense", startX1, startY+(yDifference*10));
		surface.textSize(textSize2);
		surface.text("effectiveness: ", startX1, startY+(yDifference*16));
		surface.textSize(textSize3);
		surface.text("     - to recieve most protection, you should recieve all recommended doses of vaccination" + "\n" + 
					 "     - no vaccine is 100% effective, so some people can still get sick" + "\n" + 
					 "     - CDC recommends to get vaccine as soon as one is available" + "\n" + 
					 "     - you will be fully protected 2 weeks after your second shot", startX1, startY+(yDifference*17));
		surface.textSize(textSize2);
		surface.text("after vaccination: ", startX2, startY+(yDifference));
		surface.textSize(textSize3);
		surface.text("     - should continue to wear your mask and follow social distancing guidelines \n"
				   + "       (but not required if others around you are fully vaccinated) as best you can to help protect others \n"
				   + "       who have not yet recieved the vaccine, as you could be a carrier" + "\n" + 
				     "     - outdoor activities are safer than indoor activities (but indoor activities are still allowed)" + "\n" + 
				     "     - if in US, don't need to get tested before or after travel or even self-quarantine\n"
				   + "       (if traveling outside US, make sure to check the situation of your destination)" + "\n" + 
				     "     - should still watch out for covid symptoms if you've been around someone who was/is sick", startX2, startY+(yDifference*2));
		surface.textSize(textSize2);
		surface.text("things we know about the vaccine: ", startX2, startY+(yDifference*9));
		surface.textSize(textSize3);
		surface.text("     - effective in preventing death and severe illness" + "\n" + 
					 "     - regular prevention methods(masks and social distancing) are still vital to protect others", startX2, startY+(yDifference*10));
		surface.textSize(textSize2);
		surface.text("things we don't know yet about the vaccine: ", startX2, startY+(yDifference*13));
		surface.textSize(textSize3);
		surface.text("     - how effective it is against variants" + "\n" + 
					 "     - how effective it is in people with weakened immune systems " + "\n" + 
					 "       (includes those who take immunosuppressive medications)" + "\n" +
					 "     - how long the vaccination can protect people", startX2, startY+(yDifference*14));
	}
	

	/**
	 * opens the web page in a browser
	 * @param uri URI type parameter-one that gets opened in webpage
	 * @return true or false(if opened webpage successfully or not)
	 */

	public static boolean openWebpage(URI uri) {
	    Desktop desktop = Desktop.isDesktopSupported() ? Desktop.getDesktop() : null;
	    if (desktop != null && desktop.isSupported(Desktop.Action.BROWSE)) {
	        try {
	            desktop.browse(uri);
	            return true;
	        } catch (Exception e) {
	            e.printStackTrace();
	        }
	    }
	    return false;
	}
	
	/**
	 * calls URI version of openWebPage method
	 * @param url URL type parameter-the actual url from the web browser
	 * @return true or false(if called URL version of method successfully or not)
	 */
	public static boolean openWebpage(URL url) {
	    try {
	        return openWebpage(url.toURI());
	    } catch (URISyntaxException e) {
	        e.printStackTrace();
	    }
	    return false;
	}
	
	/**
	 * @return x coordinate of this class
	 */
	public float getButtonX() {
		return buttonX;
	}
	
	/**
	 * @return y coordinate of this class
	 */
	public float getButtonY() {
		return buttonY;
	}
	
	/**
	 * @return width of buttons on page
	 */
	public int getButtonWidth() {
		return buttonWidth;
	}
	
	/**
	 * @return height of buttons on page
	 */
	public int getButtonHeight() {
		return buttonHeight;
	}
	
	/**
	 * sets the state of pfizer button to true or false
	 * @param state new state of button
	 */
	public void setPfizer(boolean state) {
		pfizerButton = state;
	}
	
	/**
	 * sets the state of johnson button to true or false
	 * @param state new state of button
	 */
	public void setJohnson(boolean state) {
		johnsonButton = state;
	}
	
	/**
	 * sets the state of moderna button to true or false
	 * @param state new state of button
	 */
	public void setModerna(boolean state) {
		modernaButton = state;
	}

}
