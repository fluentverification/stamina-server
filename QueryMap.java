package org.staminachecker.server;

import java.util.HashMap;

public class QueryMap {
	public enum QueryReturnCodes {
		SUCCESS
		, IP_IN_USE
		, IP_IS_TOR_NODE
	}
	// Maps the UID to a query
	private HashMap<String, StaminaQuery> uidToQuery;
	// Maps IP addresses to UID
	private HashMap<String, String> ipToUid;
	
	public static boolean ipLooksLikeTor(ip) {
		return false; // TODO
	}
	
	public String generateUid() {
		String uid;
		
		return uid;
	}

	/**
	 * Empty constructor.
	 * */
	public QueryMap() {
		// Intentionally left empty
	}
	
	/**
	 * Gets a query from a UID. Given an existing UID, if it does not exist,
	 * returns null pointer
	 *
	 * @param uid The Job UID
	 * @return The query information
	 * */
	public StaminaQuery getQuery(String uid) {
		if (uidToQuery.contains(uid)) {
			return uidToQuery.get(uid);
		}
		else {
			return null;
		}
	}

	/**
	 * Creates a query from information from an IP address.
	 * */
	public int createQuery(
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
		// If there is a job running for this IP, don't create a new one
		if (ipToUid.contains(ip)) {
			return IP_IN_USE;
		}
		else if (ipLooksLikeTor(ip)) {
			return IP_IS_TOR_NODE;
		}
		else {
			StaminaQuery q = new StaminaQuery(
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
			);
			String uid = this.generateUid();
			
			q.start();
		}
	}
}
