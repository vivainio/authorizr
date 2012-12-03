var oauth2_endpoints ={ 
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
	},
	"Stack exchange" : {	
		"auth_endpoint" : "https://stackexchange.com/oauth",
		"token_endpoint" : "https://stackexchange.com/oauth/access_token",
        "resource_endpoint" : "https://api.stackexchange.com/2.0",
        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback"
     },
  	"Foursquare" : {
        "auth_endpoint" : "https://foursquare.com/oauth2/authenticate",
        "token_endpoint" : "https://foursquare.com/oauth2/access_token",
        "resource_endpoint" : "https://api.foursquare.com/v2",
        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback"  		
  	},
  	"Github" : {
        "auth_endpoint" : "https://github.com/login/oauth/authorize",
        "token_endpoint" : "https://github.com/login/oauth/access_token",
        "resource_endpoint" : "https://api.github.com",
        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback"
     },
     "Instagram" : {
       	"auth_endpoint" : "https://api.instagram.com/oauth/authorize/",
        "token_endpoint" : "https://api.instagram.com/oauth/access_token",
        "resource_endpoint" : "https://api.instagram.com/v1",
        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback"
     },
     "Twitter" : {
        "auth_endpoint" : "http://api.twitter.com/oauth/request_token",
        "token_endpoint" : "http://api.twitter.com/oauth/authenticate",
        "resource_endpoint" : "",
        "redirect_uri": "http://127.0.0.1:8000/login/v1/oauth1callback"
     }
};



var oauth1_endpoints ={ 
	"Twitter":{
			"auth_endpoint":"https://api.twitter.com/oauth/authorize",			
			"user_callback_page": "http://authorizr.herokuapp.com/login/oauth1callback"
	}
};

$(function() {

	//build menu
	for(var provider in oauth2_endpoints ){
  		$("#dropdownLinksOa2").append($('<li><a href="#'+provider+'">'+provider+'</a></li>'));
    }
	          
    $("#dropdownLinksOa2 a").click(function(event) {
    
    	event.preventDefault();
  		
  		key = $(this).attr('href').substring(1); 		  		   		
  		
  		endpoint = oauth2_endpoints[key];	    
  		     	
     	for(var k in endpoint ){	     
      		$("#id_oa2-"+k).val(endpoint[k]);
    	}
    });
    
    //build menu
	for(var provider in oauth1_endpoints ){
  		$("#dropdownLinksOa1").append($('<li><a href="#'+provider+'">'+provider+'</a></li>'));
    }
	          
    $("#dropdownLinksOa1 a").click(function(event) {
    
    	event.preventDefault();
  		
  		key = $(this).attr('href').substring(1); 		  		   		
  		
  		endpoint = oauth1_endpoints[key];	    
  		     	
     	for(var k in endpoint ){	     
      		$("#id_oa1-"+k).val(endpoint[k]);
    	}
    });
});
