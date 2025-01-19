import java.awt.Point;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

import processing.core.PApplet;

/**

	Represents a Game Of Life grid.

	Coded by: Nodoka Shibasaki
	Modified on: 3.29.2021

*/

public class Life {

	// Add a 2D array field to represent the Game Of Life grid.
	
	boolean[][] grid;
	
	
	/**
	 * Initialized the Game of Life grid to an empty 20x20 grid.
	 */
	public Life() {
		grid = new boolean[20][20];
	}

	
	
	/**
	 * Initializes the Game of Life grid to a 20x20 grid and fills it with data from the file given.
	 * 
	 * @param filename The path to the text file.
	 */
	public Life(String filename) {
		grid = new boolean[20][20];
		readData(filename, grid);
//		System.out.println(this);
//		this.step();
//		System.out.println(this);
	}
	
	/**
	 * Runs a single step within the Game of Life by applying the Game of Life rules on
	 * the grid.
	 */
	public void step() {
		
		//int[][] num = new int[grid.length][grid[0].length];
		boolean[][] gen = new boolean[grid.length][grid[0].length];
		
		for(int x = 1; x < grid.length -1; x ++) {
			for(int y = 1; y < grid[0].length - 1; y ++) {
				
				int neighbors = 0;
				
				for(int i = -1; i <= 1; i++) {
					for(int j = -1; j <= 1; j++) {
						if(grid[x+i][y+j]) {
							neighbors ++;
						}
					}
				}
				
				if(grid[x][y]) {
					neighbors --;
				}
				
				if(neighbors < 2 && grid[x][y]) {
					gen[x][y] = false;
				}else if(neighbors > 3 && grid[x][y]) {
					gen[x][y] = false;
				}else if(neighbors == 3 && !grid[x][y]) {
					gen[x][y] = true;
				}else {
					gen[x][y] = grid[x][y];
				}
				
			}
		}
		
		grid = gen;
		
//		for(int i = 0; i < grid.length; i++) {
//			for(int j = 0; j < grid[0].length; j++) {
//				int x = countNeighbors(i, j);
//				
//				num[i][j] = x;
//				
//				System.out.print(x);
//				
//				if(j == grid.length-1) {
//					System.out.print('\n');
//				}
//			}
//		}
//		
//		for(int i = 0; i < grid.length; i++) {
//			for(int j = 0; j < grid[0].length; j++) {
//				if(num[i][j] < 2) {
//					grid[i][j] = false;
//				}else if(num[i][j] > 3) {
//					grid[i][j] = false;
//				}else if(num[i][j] == 3) {
//					grid[i][j] = true;
//				}
//			}
//		}
	}

	
	
	/**
	 * Runs n steps within the Game of Life.
	 * @param n The number of steps to run.
	 */
	public void step(int n) {
		for(int i = n; i > 0; i--) {
			step();		
		}
	}
	
	
	
	/**
	 * Formats this Life grid as a String to be printed (one call to this method returns the whole multi-line grid)
	 * 
	 * @return The grid formatted as a String.
	 */
	public String toString() {
		
		String output = "";
		
		for(int i = 0; i < grid.length; i++) {
			for(int j = 0; j < grid[i].length; j++) {
				if(grid[i][j]) {
					output += "*";
				}else {
					output += "-";
				}
			}
			output += '\n';
		}
		
		return output;
	}
	
	
	
	/**
	 * (Graphical UI)
	 * Draws the grid on a PApplet.
	 * The specific way the grid is depicted is up to the coder.
	 * 
	 * @param marker The PApplet used for drawing.
	 * @param x The x pixel coordinate of the upper left corner of the grid drawing. 
	 * @param y The y pixel coordinate of the upper left corner of the grid drawing.
	 * @param width The pixel width of the grid drawing.
	 * @param height The pixel height of the grid drawing.
	 */
	public void draw(PApplet marker, float x, float y, float width, float height) {
		marker.noFill();
		for(int i = 0; i < grid.length; i++) {
			for(int j = 0; j < grid[0].length; j++) {
				float w = width/grid[0].length;
				float h = height/grid.length;
				float dx = x + j * w;
				float dy = y + i * h;
				if(grid[i][j]) {
					marker.fill(0);
				}else {
					marker.fill(255);
				}
				marker.rect(dx, dy, w, h);
			}
		}
	}
	
	
	
	/**
	 * (Graphical UI)
	 * Determines which element of the grid matches with a particular pixel coordinate.
	 * This supports interaction with the grid using mouse clicks in the window.
	 * 
	 * @param p A Point object containing a graphical pixel coordinate.
	 * @param x The x pixel coordinate of the upper left corner of the grid drawing. 
	 * @param y The y pixel coordinate of the upper left corner of the grid drawing.
	 * @param width The pixel width of the grid drawing.
	 * @param height The pixel height of the grid drawing.
	 * @return A Point object representing a coordinate within the game of life grid.
	 */
	public Point clickToIndex(Point p, float x, float y, float width, float height) {
		
		double px = p.getX();
		double py = p.getY();
		
		double w = width/grid[0].length;
		double h = height/grid.length;
		double dx = (int)((px-x)/w);
		double dy = (int)((py-y)/h);
				
		if(dx >= 0 && dx < grid.length && dy >= 0 && dy < grid[0].length) {
			 Point p2 = new Point();
			 p2.setLocation(dy, dx);
			 return p2;
		}
				
		return null;
	}
	
	/**
	 * (Graphical UI)
	 * Toggles a cell in the game of life grid between alive and dead.
	 * This allows the user to modify the grid.
	 * 
	 * @param i The x coordinate of the cell in the grid.
	 * @param j The y coordinate of the cell in the grid.
	 */
	public void toggleCell(int i, int j) {
		grid[i][j] = !grid[i][j];
	}

	

	// Reads in array data from a simple text file containing asterisks (*)
	public void readData (String filename, boolean[][] gameData) {
		File dataFile = new File(filename);

		if (dataFile.exists()) {
			int count = 0;

			FileReader reader = null;
			Scanner in = null;
			try {
				reader = new FileReader(dataFile);
				in = new Scanner(reader);

				while (in.hasNext()) {
					String line = in.nextLine();
					for(int i = 0; i < line.length(); i++)
						if (count < gameData.length && i < gameData[count].length && line.charAt(i)=='*')
							gameData[count][i] = true;

					count++;
				}
			} catch (IOException ex) {
				throw new IllegalArgumentException("Data file " + filename + " cannot be read.");
			} finally {
				if (in != null)
					in.close();
			}

		} else {
			throw new IllegalArgumentException("Data file " + filename + " does not exist.");
		}
	}



	
	
}