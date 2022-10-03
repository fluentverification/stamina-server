import java.net.URI;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

// Our classes
import org.staminachecker.server.StaminaQueries;
import org.staminachecker.server.StaminaQuery;
import org.staminachecker.server.StaminaQueryMap;

@RestController
@RequestMapping(path = "/queries")
public class StaminaController {

	@Autowired
	private StaminaQueries staminaQueries;
	
	/**
	 * Gets updates for a specific UID. Given a UID, gets any updates from the log
	 * */
	@GetMapping(
		path = "/"
		, produces = "application/json"
		, consumes = "application/json"
	)
	public String getUpdate(@RequestBody String uid) {
		// TODO
	}
	
	@PostMapping(
		path = "/"
		, produces = "application/json"
		, consumes = "application/json"
	)
	public ResponseEntity<Object> startJob(@RequestBody StaminaQuery query) {
		// TODO
	}
}
