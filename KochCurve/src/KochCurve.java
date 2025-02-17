import processing.core.PApplet;


/**
  @(#)KochCurve.java


  @author
  @version
*/
public class KochCurve {

	// TO DO
	private int level;
	private double length;
	private double x;
	private double y;
	private double angle;
	

    public KochCurve(int level, int length) {
    	this.level = level;
    	this.length = length;
    	x = 150;
    	y = 50;
    	angle = 0;
    }
    
    public KochCurve(int level, int length, double x, double y, double angle) {
    	this.level = level;
    	this.length = length;
    	this.x = x;
    	this.y = y;
    	this.angle = angle;
    }
    
    public void draw(PApplet marker) {
    	if(angle < 0) {
    		drawKochCurve(marker, level, length, x, y, angle);
    	}else {
    		drawKochCurve(marker, level, length, x, y, angle + Math.PI);
    	}
    }

    private void drawKochCurve(PApplet marker, int level, double length, double x, double y, double angle) {
		double dx = Math.cos(angle) * length;
		double dy =  Math.sin(angle) * length;
    	if(level < 1) {
    		marker.line((float)x, (float)y, (float)(x + dx), (float)(y + dy));
    	}else {
    		double ax = x + dx / 3;
    		double ay = y + dy / 3;
    		double bx = x + dx * 2 / 3;
    		double by = y + dy * 2 / 3;
    		double h = Math.sqrt(3) / 2 * length / 3;
    		double cx = x + dx / 2 - Math.sin(angle) * h;
    		double cy = y + dy / 2 + Math.cos(angle) * h;

    		drawKochCurve(marker, level-1, length/3, x, y, angle);
    		drawKochCurve(marker, level-1, length/3, ax, ay, angle + Math.PI / 3);
    		drawKochCurve(marker, level-1, length/3, bx, by, angle);
    		drawKochCurve(marker, level-1, length/3, cx, cy, angle - Math.PI / 3);
    		
    	}
    }

}
