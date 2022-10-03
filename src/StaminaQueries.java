package org.staminachecker.server;

import org.staminachecker.server.StaminaQueryMap;

import org.springframework.stereotype.Repository;

@Repository

public class StaminaQueries {
	private static StaminaQueryMap qMap = new StaminaQueryMap();
	
	public static void createQuery(
		String ip
		, String modelFile
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
		int queryResponse = qMap.createQuery(
			ip
			, modelFile
			, propertiesFile
			, method
			, threads
			, kappa
			, rkappa
			, window
			, transitionFile
			, labels                                                                                      
			, stateLimit
		);
	}
}
