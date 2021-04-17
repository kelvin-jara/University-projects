package Communications.testing;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.CoreMatchers.not;
import org.junit.jupiter.api.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ServerTest {

	@BeforeEach
	void setUp() throws Exception {
		
	}

	@Test
	void testServer() throws UnknownHostException, IOException {
		var sock = new Socket(InetAddress.getByName("127.0.0.1"), 8888);
		try (var out = new PrintWriter(sock.getOutputStream());
		       var in = new BufferedReader(new InputStreamReader(sock.getInputStream()))) {
		    String name = "Kelvin";
			// Send hello
		    out.println("HELLO~" + name);
		    out.flush();
		    assertThat(in.readLine(), containsString("HELLO"));
		    //Login to server
		    out.println("LOGIN~" + name);
		    out.flush();
		    assertThat(in.readLine(), containsString("LOGIN"));	
		    // Get in queue
		    out.println("QUEUE");
		    out.flush();
		    String line = in.readLine(); 
		    assertThat(line, containsString(""));
		    //List the players
		    out.println("LIST");
		    out.flush();
		    String line2 = in.readLine(); 
		    assertThat(line2, containsString("LIST~Kelvin"));
		    // Get out of List
		    out.println("QUEUE");
		    out.flush();
		    String line3 = in.readLine(); 
		    assertThat(line3, containsString(""));
		    // Check in a second guest
		    out.println("LIST");
		    out.flush();
		    //assertThat(in.readLine(), containsString(name));
		    assertEquals(in.readLine(), "LIST");
		    
		   }
	}

}
