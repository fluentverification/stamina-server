package org.staminachecker.server;

public class StaminaQuery {
	public enum METHODS {
		ITERATIVE
		, PRIORITY
		, RE_EXPLORING
	}
	/**
	 * Empty Query
	 * */
	public StaminaQuery() {
		// Intentionally left empty
	}
	
	/**
	 * Main constructor. Creates a StaminaQuery object with
	 * various parameters
	 *
	 * @param modelFile The contents of the model file
	 * @param propertiesFile The contents of the properties file
	 * @param method The method to use
	 * @param threads The number of threads to use
	 * @param kappa The value for the reachability threshold
	 * @param rkappa The value for kappa to be reduced by
	 * @param window The window size (max value of Pmax - Pmin)
	 * @param transitionFile Whether to create a transition file
	 * @param labels Whether to print label information
	 * @param stateLimit The absolute state limit to use
	 * */
	public StaminaQuery(
		String modelFile
		, String propertiesFile
		, int method
		, int threads
		, double kappa
		, double rkappa
		, double window
		, boolean transitionFile
		, boolean labels
		, int stateLimit
	) {
		this.modelFile = modelFile;
		this.propertiesFile = propertiesFile;
		this.method = method;
		this.threads = threads;
		this.kappa = kappa;
		this.rkappa = rkappa;
		this.window = window;
		this.transitionFile = transitionFile;
		this.labels = labels;
		this.stateLimit = stateLimit;

	}

	/**
	* Gets the value of modelFile
	* @return The value of modelFile 
	* */
	public String getModelFile() {
		return this.modelFile;
	}

	/**
	* Sets the value of modelFile
	* @param modelFile The value to set this.modelFile to
	* */
	public void setModelFile(String modelFile){
		this.modelFile = modelFile;
	}
	

	/**
	* Gets the value of propertiesFile
	* @return The value of propertiesFile 
	* */
	public String getMropertiesFile() {
		return this.propertiesFile;
	}

	/**
	* Sets the value of propertiesFile
	* @param propertiesFile The value to set this.propertiesFile to
	* */
	public void setMropertiesFile(String propertiesFile){
		this.propertiesFile = propertiesFile;
	}
	

	/**
	* Gets the value of method
	* @return The value of method 
	* */
	public int getMethod() {
		return this.method;
	}

	/**
	* Sets the value of method
	* @param method The value to set this.method to
	* */
	public void setMethod(int method){
		this.method = method;
	}
	

	/**
	* Gets the value of threads
	* @return The value of threads 
	* */
	public int getMhreads() {
		return this.threads;
	}

	/**
	* Sets the value of threads
	* @param threads The value to set this.threads to
	* */
	public void setMhreads(int threads){
		this.threads = threads;
	}
	

	/**
	* Gets the value of kappa
	* @return The value of kappa 
	* */
	public double getMappa() {
		return this.kappa;
	}

	/**
	* Sets the value of kappa
	* @param kappa The value to set this.kappa to
	* */
	public void setMappa(double kappa){
		this.kappa = kappa;
	}
	

	/**
	* Gets the value of rkappa
	* @return The value of rkappa 
	* */
	public double getMkappa() {
		return this.rkappa;
	}

	/**
	* Sets the value of rkappa
	* @param rkappa The value to set this.rkappa to
	* */
	public void setMkappa(double rkappa){
		this.rkappa = rkappa;
	}
	

	/**
	* Gets the value of window
	* @return The value of window 
	* */
	public double getMindow() {
		return this.window;
	}

	/**
	* Sets the value of window
	* @param window The value to set this.window to
	* */
	public void setMindow(double window){
		this.window = window;
	}
	

	/**
	* Gets the value of transitionFile
	* @return The value of transitionFile 
	* */
	public boolean getMransitionFile() {
		return this.transitionFile;
	}

	/**
	* Sets the value of transitionFile
	* @param transitionFile The value to set this.transitionFile to
	* */
	public void setMransitionFile(boolean transitionFile){
		this.transitionFile = transitionFile;
	}
	

	/**
	* Gets the value of labels
	* @return The value of labels 
	* */
	public boolean getMabels() {
		return this.labels;
	}

	/**
	* Sets the value of labels
	* @param labels The value to set this.labels to
	* */
	public void setMabels(boolean labels){
		this.labels = labels;
	}
	

	/**
	* Gets the value of stateLimit
	* @return The value of stateLimit 
	* */
	public int getMtateLimit() {
		return this.stateLimit;
	}

	/**
	* Sets the value of stateLimit
	* @param stateLimit The value to set this.stateLimit to
	* */
	public void setMtateLimit(int stateLimit){
		this.stateLimit = stateLimit;
	}

	// model and properties file
	// contains the contents
	private String modelFile;
	private String propertiesFile;
	// method and multithreading
	private int method;
	private int threads;
	// main params
	private double kappa;
	private double rkappa;
	private double window;
	// additional options
	private boolean transitionFile;
	private boolean labels;
	private int stateLimit;

}
