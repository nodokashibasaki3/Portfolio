package statistics;

import java.awt.Point;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.text.ParseException;
import java.time.Duration;
import java.time.LocalDate;
import java.time.Period;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;

import javax.imageio.ImageIO;
import javax.swing.JButton;

import processing.core.PApplet;

/**
 * This class gets creates graohics for the individual state classes including graphs and statistics.
 * 
 * @author nodoka shibasaki
 *
 */
public class StatesGraphics{
	
	private Stats stat;	
	private String name;
	private double PIXEL_PER_Y, PIXEL_PER_X;
	
	private double graphWidth, graphHeight;
	
	private ArrayList<Double> cases, deaths, vaccineList, prediction;
	private ArrayList<String> vaccine, vaccineDates, covidDates;
	private ArrayList<Point> points, points2, points3, points4;
	
	private boolean infoAvailable;
	
	private Timer timer;
	
	/**constructor
	 * if no parameter is inputted, the name is set to null
	 */
	public StatesGraphics() {
		this(null);
		Timer timer = new Timer();
		timer.schedule(new Stats(), 1000000);
	}
	
	/**constructor
	 * sets the name to the parameter String state
	 * @param state state that the graphics are being drawn for
	 */
	public StatesGraphics(String state) {
		stat = new Stats();
		name = state;
		Timer timer = new Timer();
		timer.schedule(new Stats(), 1000000);
	}
	
	

	/**returns the name of the state
	 * @return name String
	 */
	public String getName() {
		return name;
	}
	
	/**
	 * predicts data for the next 14 days based on the fully vaccinated population,
	 * vaccinated once population and the spread rate of covid-19. It also subtracts 
	 * the patients from 14 days ago because the average cure/death rate is 14 days.
	 * 
	 * @return array of predicted data sets
	 */
	public ArrayList<Double> predictData(){
		
		vaccine = stat.getLatestVaccineInfo(name);	
		prediction = new ArrayList<Double>();
		
		if(vaccine.size() > 8 && vaccine != null && cases.size() > 0) {
			if(!vaccine.get(8).equals("") && !vaccine.get(5).equals("")) {
				double full = Double.parseDouble(vaccine.get(7));
				double one = Double.parseDouble(vaccine.get(3));
				
				prediction.add(cases.get(cases.size()-1));

				for(int i = 0; i < 14; i++) {
					
					double casesFifteen = cases.get(cases.size()-(15 - i));
					double casesFourteen = cases.get(cases.size()-(14 - i));
					double diff = casesFifteen - casesFourteen;
									
					if(diff < 0) {
						diff = 0;
					}
					
					double pred = (prediction.get(i) * 2) - (full) - (one * 0.9) - diff;
								
					if(pred > prediction.get(i)) {
						prediction.add(pred);
					}else {
						prediction.add(prediction.get(i));
					}
				}
								
				
			}
			
		}
	
		return prediction;
	}
	
	
	
	/**
	 * draws graph by figuring out all points of where the graph needs to be plotted.
	 * 
	 * @param p PApplet graph is being drawn on
	 * @param x x coordinate of the left up corner of where the graph is drawn
	 * @param y y coordinate of the left up corner of where the graph is drawn
	 * @param stateName name of state graph is being created for
	 * @throws ParseException 
	 */
	public void createGraph(PApplet p, double x, double y, String stateName){
		
		cases = stat.getDoubleData(name, 3, "data/cases.csv");
		deaths = stat.getDoubleData(name, 4, "data/cases.csv");
		covidDates = stat.getStringData(name, 0, "data/cases.csv");
		vaccineDates = stat.getStringData(name, 0, "data/vaccineNumber.csv");
		vaccineList = stat.getDoubleData(name, 7, "data/vaccineNumber.csv");
		prediction = predictData();
		
		boolean graphingVaccine = true;
		
		if(vaccineList.size() <= 0) {
			graphingVaccine = false;
		}
		
		//figure out the biggest number of the arraylist to scale y
		double b = cases.get(0); //write this as a text on top of the yaxis
		
		for(int i = 1; i < cases.size(); i++) {
			if(b < cases.get(i)) {
				b = cases.get(i);
			}
			
			if(i < vaccineList.size()) {
				if(b < vaccineList.get(i)) {
					b = vaccineList.get(i);
				}
			}

		}
		
		DateTimeFormatter DATEFORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");
		
		LocalDate firstDate = LocalDate.parse(covidDates.get(0), DATEFORMATTER);
		LocalDate lastDate = LocalDate.parse(covidDates.get(covidDates.size()-1), DATEFORMATTER);
				 
		//draw the frame of the graph
		p.line((float)x + 10, (float)y, (float)x + 10, (float)(y + graphHeight - 10));
		p.line((float)x+10, (float)(y + graphHeight - 10), (float)(x + graphWidth - 10), (float)(y + graphHeight - 10));
		
		p.fill(0);
		p.textSize(10);
		p.text((int)b + "", (float)x - 30, (float)y);

		for(int i = 1; i < 7; i++) {
			p.text((int)(b * (7 - i) / 7)  + "", (float)x - 30, (float)(y + ((graphHeight - 10) * i / 7)));
		}
		
		p.text(covidDates.get(0), (float)(x), (float)(y + graphHeight - 5));
		p.text(covidDates.get(covidDates.size()-1), (float)(x - 10 + graphWidth), (float)(y + graphHeight - 5));

		p.textSize(12);
		p.text("# of covid cases in " + name, (float)(x + (graphWidth - 10)/2), (float)((y - 10)));
		p.text("date", (float)(x + ( graphWidth - 10)/2), (float)((y + graphHeight)));
		p.text("population", (float)((x - 70)), (float)(y + (graphHeight - 10)/2));
		p.fill(0, 0, 255);
		p.text("population of covid-19 cases in " + name, (float)(x + 10), (float)((y + graphHeight + 10)));
		 
		p.fill(255, 0, 0);
		p.text("population of covid-19 deaths in " + name, (float)(x + 10), (float)((y + graphHeight + 25)));
		
		p.fill(0, 255, 0);
		p.text("population of fully vaccinated in " + name, (float)(x + 10), (float)((y + graphHeight + 40)));

		p.fill(255, 165, 0);
		p.text("predicted covid-19 cases in " + name, (float)(x + 10), (float)((y + graphHeight + 55)));

		PIXEL_PER_X = (graphWidth - 10) / (covidDates.size());
		
		if(graphingVaccine) {
			int diff = 0;
			
			for(int i = 0; i < covidDates.size(); i++) {
				if(covidDates.get(i).equals(vaccineDates.get(0))) {
					diff = i;
				}
			}
			
			PIXEL_PER_X = (graphWidth - 10) / (vaccineDates.size() + diff);

		}
		
		//number in each pixel
		PIXEL_PER_Y = (graphHeight - 10) / b;
		
		//coordinate of the base of the lines
		double xAxis = x + 10;
		double yAxis = y + graphHeight - 10;
		
		
		
		//add one day to first date and check if index of that date is existing
		//keep track of how many days added
		//if it is existing access the value at the same index in case data
		//figure out the coordinates
		
		double initial = 0.0;
		
		if(graphingVaccine) {
			initial = PIXEL_PER_X * covidDates.indexOf(vaccineDates.get(0));
		}
		
		double predInitial = PIXEL_PER_X * covidDates.size();
		
		points = new ArrayList<Point>();
		points2 = new ArrayList<Point>();
		points3 = new ArrayList<Point>();
		points4 = new ArrayList<Point>();

		while(!firstDate.equals(lastDate)) {
				
				if(covidDates.indexOf(firstDate.toString()) != -1) {
					double px = xAxis + PIXEL_PER_X * covidDates.indexOf(firstDate.toString());
					double py = yAxis - PIXEL_PER_Y * cases.get(covidDates.indexOf(firstDate.toString())) ;
					Point po = new Point();
					po.setLocation(px, py);
					points.add(po);
				}
				
				if(covidDates.indexOf(firstDate.toString()) != -1) {
					double py = yAxis - PIXEL_PER_Y * deaths.get(covidDates.indexOf(firstDate.toString())) ;
					double px = xAxis + PIXEL_PER_X * covidDates.indexOf(firstDate.toString());
					Point po = new Point();
					po.setLocation(px, py);
					points2.add(po);
				}
				
				if(graphingVaccine && vaccineList.size() > vaccineDates.indexOf(firstDate.toString())) {
					if(vaccineDates.indexOf(firstDate.toString()) != -1) {
						double py = yAxis - PIXEL_PER_Y * vaccineList.get(vaccineDates.indexOf(firstDate.toString())) ;
						
						double px = xAxis + initial + PIXEL_PER_X * vaccineDates.indexOf(firstDate.toString());
						Point po = new Point();
						po.setLocation(px, py);
						points3.add(po);
					}
				}
				
				
			firstDate = firstDate.plusDays(1);
		}
		
		for(int i = 0; i < prediction.size(); i++) {
			
			double py = yAxis - PIXEL_PER_Y * prediction.get(i) ;
			double px = xAxis + predInitial + PIXEL_PER_X * i;
			Point po = new Point();
			po.setLocation(px, py);
			points4.add(po);
			
		}

		for(int i = 0; i < points.size()-1; i++) {
	
			//deaths
			p.stroke(255, 0, 0);
			p.fill(139, 0, 0);
			p.line((float)points2.get(i).getX(), (float)points2.get(i).getY(), (float)points2.get(i+1).getX(), (float)points2.get(i+1).getY());
			
			if(i % 10 == 0)
				p.circle((float)points2.get(i).getX(), (float)points2.get(i).getY(), (float)PIXEL_PER_X * 3);

			//cases
			p.stroke(0, 0, 255);
			p.fill(0, 0, 139);
			p.line((float)points.get(i).getX(), (float)points.get(i).getY(), (float)points.get(i+1).getX(), (float)points.get(i+1).getY());
			
			if(i % 10 == 0)
				p.circle((float)points.get(i).getX(), (float)points.get(i).getY(), (float)PIXEL_PER_X * 3);
			
			//vaccination
			if(i < points3.size()-2) {
				p.stroke(0, 255, 0);
				p.fill(0, 139, 0);
				p.line((float)points3.get(i).getX(), (float)points3.get(i).getY(), (float)points3.get(i+1).getX(), (float)points3.get(i+1).getY());
					
				if(i % 10 == 0)
					p.circle((float)points3.get(i).getX(), (float)points3.get(i).getY(), (float)PIXEL_PER_X * 3);
			}
			
			//prediction
			if(i < points4.size()-2) {
				p.stroke(255, 165, 0);
				p.fill(230, 126, 0);
				p.line((float)points4.get(i).getX(), (float)points4.get(i).getY(), (float)points4.get(i+1).getX(), (float)points4.get(i+1).getY());
				
			}
						
		}
			
		p.stroke(0,0,0);
		p.noFill();
		
		//saving the graph as a png image
		if (p.height<p.width) {
			graphWidth = (p.height/2);
			graphHeight = (p.height/2);
		} else {
			graphWidth = (p.width/2);
			graphHeight = (p.width/2);
		}
		
		p.save("graphs/"+stateName+".png");
		try {
			BufferedImage source = ImageIO.read(new File("graphs/"+stateName+".png")) ;
			BufferedImage croppedImage = source.getSubimage((int) (7*(p.width/11)-(0.4*graphWidth)), (int) (p.height/20-(0.1*graphHeight)), (int)(1.5*graphWidth), (int)(1.3*graphHeight));
			ImageIO.write(croppedImage, "png", new File("graphs/"+stateName+".png"));
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

	}
	
	
	public void draw (PApplet surface) {

		if (surface.height<surface.width) {
			graphWidth = (surface.height/2);
			graphHeight = (surface.height/2);
		} else {
			graphWidth = (surface.width/2);
			graphHeight = (surface.width/2);
		}

		writeInfo(surface, (surface.width/20) , surface.height* 11 /20, (float)surface.height/45, (float)surface.height/60, (float)surface.height/50);
		showGraphCoordinates(surface, PIXEL_PER_X * 3, points, points2, points3);

	}
	
	/**
	 * writes recent information of the state vaccination situation including
	 * the name of the vaccines, number of doses availbale, population vaccinated and
	 * people fully vaccinated.
	 * 
	 * @param p PApplet to draw on
	 * @param x x coordinates of center of all texts
	 * @param y y coordinates of the top of where the text starts
	 */
	private void writeInfo(PApplet p, double x, double y, float titleSize, float writingSize, float leading) {
		
		p.fill(0);
		p.textSize(titleSize);
		p.textAlign(p.LEFT);
		
		if(vaccine.size() > 13){
			infoAvailable = true;

		} else {
			infoAvailable = false;
			p.text("there is no numerical vaccination data available for " + name, (float)x, (float)(y + 30));
		}
		p.textAlign(p.CENTER);
		p.text("all data updated as of " + covidDates.get(covidDates.size()-1), (float)(p.width/4*3), (float)(p.height  / 4*3));
		p.textAlign(p.LEFT);

	}
	
	/**
	 * 
	 * @param p PApplet to draw on
	 * @param diameter diameter of the circle hovered on
	 * @param p1 arraylist of points of death of covid 19
	 * @param p2 arraylist of points of cases of covid 19
	 * @param p3 arraylist of points of 
	 */
	private void showGraphCoordinates(PApplet p, double diameter, ArrayList<Point> p1, ArrayList<Point> p2, ArrayList<Point> p3) {
		//if mouseX mouseY is in one of the points range then show the text
		double x = p.mouseX;
		double y = p.mouseY;
		
		String text = "";
		
		for(int i = 0; i < p1.size(); i++) {
			
			if(x >= p1.get(i).getX()-diameter/2 && x <= p1.get(i).getX() + diameter * 1.5 && y >= p1.get(i).getY()-diameter/2 && y <= p1.get(i).getY()+diameter*1.5) {
				text = "(" + deaths.get(i) + " on " + covidDates.get(i) + ")";
			}else if(x >= p2.get(i).getX()-diameter/2 && x <= p2.get(i).getX() + diameter * 1.5 && y >= p2.get(i).getY()-diameter/2 && y <= p2.get(i).getY()+diameter*1.5) {
				text = "(" + cases.get(i) + " on " + covidDates.get(i) + ")";
			}else if(i < vaccineList.size() && i < p3.size()) {
				if(x >= p3.get(i).getX()-diameter/2 && x <= p3.get(i).getX() + diameter * 1.5 && y >= p3.get(i).getY()-diameter/2 && y <= p3.get(i).getY()+diameter*1.5)
					text = "(" + vaccineList.get(i) + " on " + vaccineDates.get(i) + ")";
			}

		}
		p.textSize(p.height/60);
		p.fill(0);
		p.text(text, 850, 100); 
	}
	
	
	//get methods
		
	/**
	 * gets info available boolean
	 * @return infoAvailable in the instance field
	 */
	public boolean getInfoAvailable() {
		return infoAvailable;
	}
	
	/**
	 * gets arraylist of strings of latest vaccine info
	 * @return vaccine the latest vaccine info
	 */
	public ArrayList<String> getVaccineInfo(){
		return vaccine;
	}
	
	/**
	 * gets width of the graph drawn
	 * @return graphWidth
	 */
	public double getGraphWidth() {
		return graphWidth;
	}

	/**
	 * gets height of the graph drawn
	 * @return graphHeight
	 */
	public double getGraphHeight() {
		return graphHeight;
	}


}
