
# WIKI 2.0

Wiki 2.0 is a reimagined and revamped version of Wikipedia using Wikipedia's free and public *[MediaWiki REST API]( https://www.mediawiki.org/wiki/API:REST_API)*. The goal of this project is to create a simple more convenient version of Wikipedia that will maximize user efficiency and simplicity without hindering functionality.

## MediaWiki REST API

Wiki 2.0 was created using the *[MediaWiki REST API]( https://www.mediawiki.org/wiki/API:REST_API)*. This API allows the user to make requests and return a response in the form of objects such as *[page objects](https://www.mediawiki.org/wiki/API:REST_API/Reference#Example_2)* like the one shown below. 
		  
	{
	  "id":  9228,
	  "key":  "Earth",
	  "title":  "Earth",
	  "latest":  {
	  "id":  963613515,
	  "timestamp":  "2020-06-20T20:05:55Z"
	  },
	  "content_model":  "wikitext",
	  "license":  {
	  "url":  "//creativecommons.org/licenses/by-sa/3.0/",
	  "title":  "Creative Commons Attribution-Share Alike 3.0"
	  },
	  "html_url":   "https://en.wikipedia.org/w/rest.php/v1/page/Earth/html"
	}

It is with this response information a user can determine what is done with and how the information is used. For Wiki 2.0, the decision was made to keep simplistic functionality for a smooth and altered *[Wikipedia](https://www.wikipedia.org/)* experience. 

## Wiki 2.0 Functionality 

The application is intended to work with users in allowing them to efficiently and effectively browse new terminology and immerse themselves in useful topics. This application will allow a new user to quickly setup and create a new account, once completed the user will have access to a couple of features such as the ability to track most recent searches and even add a searched article to their favorites for future browsing and discovery. 

## Tools Used 

This application was created using the following tools:

- Flask 
- WTForms
- PostgreSQL
- SQLAlchemy

Other useful libraries used include:

- Bcrypt
- datetime