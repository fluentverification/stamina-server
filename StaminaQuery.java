package org.staminachecker.online;

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
