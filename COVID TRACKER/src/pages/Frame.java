package pages;
/**The frame of the classes with pictures, CountryMap and State
* @author sophie
*/
import processing.core.PApplet;

/**the frame of the state and the country page
 * creates the frame
 * @author sophie lin
 *
 */
public class Frame{
	
	private String fileName;
	
	/**
	 * no-args constructor initializes field
	 * @param name state name
	 */
	public Frame(String name) {
		fileName = name;
	}
	/**
	 * draws the drop down button for each page in state or map
	 * @param surface PApplet
	 * @param screenWidth width of the window
	 */
	public void drawDropDownButton(PApplet surface, int screenWidth) {
		surface.strokeWeight(5);
		surface.line(screenWidth-40, 10, screenWidth-10, 10);
		surface.line(screenWidth-40, 20, screenWidth-10, 20);
		surface.line(screenWidth-40, 30, screenWidth-10, 30);
		surface.strokeWeight(1);
	}
	/**
	 * draws the back button for state and country
	 * @param surface PApplet 
	 * @param screenWidth  width of the window
	 * @param screenHeight height of the window
	 */
	public void drawBackButton(PApplet surface, int screenWidth, int screenHeight) {
		surface.rect(surface.width-surface.width/25-surface.width/100, surface.height-surface.height/25-surface.height/100, surface.width/25, surface.height/25);
	}
}
