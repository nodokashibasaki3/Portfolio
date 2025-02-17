import processing.core.PApplet;

public class KochSnowflake {
	private int level;
	private double length;
	private KochCurve koch1, koch2, koch3;

    public KochSnowflake(int level, int length) {
    	this.level = level;
    	this.length = length;
    	koch1 = new KochCurve(this.level, length, 100, 200, Math.PI);
    	koch2 = new KochCurve(this.level, length, 100 + length / 2, 200 - length / 2 * Math.sqrt(3), -4*Math.PI/3);
    	koch3 = new KochCurve(this.level, length, 100 + length, 200, Math.PI/3);
    }
    
    public void draw(PApplet marker) {
    	drawKochSnowflake(marker, level, length, 200, 100, 180);
    }

    private void drawKochSnowflake(PApplet marker, int level, double length, double x, double y, double angle) {
    	
    	koch1.draw(marker);
    	koch2.draw(marker);
    	koch3.draw(marker);
//    	double newX = Math.cos(angle);
//		double newY = Math.sin(angle);
//		double dx = newX * length;
//		double dy = newY * length;
//    	
//    	if(level < 1) {
//    		marker.line((float)x, (float)y, (float)(x + dx), (float)(y + dy));
//    		marker.line((float)(x + dx), (float)(y + dy), (float)(x + (dx*2)), (float)y);
//    		marker.line((float)(x + (dx*2)), (float)y, (float)x, (float)y);
//    	}else {
//    		this.level--;
//    		this.length/=3;
//    		
//    		koch1.draw(marker);
//    		koch2.draw(marker);
//    		koch3.draw(marker);
// 
//    	}
    }
}
