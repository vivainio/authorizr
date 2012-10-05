var endpoints ={ 
	"Google":{
			"auth_endpoint":"https://accounts.google.com/o/oauth2/auth",
			"token_endpoint":"https://accounts.google.com/o/oauth2/token",
			"resource_endpoint":"https://www.googleapis.com/oauth2/v1",
			"redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback",
			"scope": "https://www.googleapis.com/auth/userinfo.profile "
	},
	
	"Facebook":{
		 	"auth_endpoint" : "https://www.facebook.com/dialog/oauth",
	        "token_endpoint" : "https://graph.facebook.com/oauth/access_token",
	        "resource_endpoint" : "https://graph.facebook.com",
	        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback"   
	}	
};


$(function() {

	//build menu
	for(var provider in endpoints ){
  		$("#dropdownLinks").append($('<li><a href="#'+provider+'">'+provider+'</a></li>'));
    }
	          
    $("#dropdownLinks a").click(function(event) {
    
    	event.preventDefault();
  		
  		key = $(this).attr('href').substring(1); 		  		   		
  		
  		endpoint = endpoints[key];	    
  		     	
     	for(var k in endpoint ){	     
      		$("#id_"+k).val(endpoint[k]);
    	}
    	
    });
    
});
