var
  http = require('http'),
  fs = require('fs'),
  path = require('path'),
  url = require('url');

function main() {
  var
    PORT = 8080;

	var server = http.createServer(function(request, response) {
		console.log('requesting "%s"', request.url);
		
    var urlParts = url.parse( request.url );

		var root = ".";
		var filePath = path.join( '.', urlParts.pathname );
		if (filePath === './') {
			filePath = './index.html';
    }
	
		var extname = path.extname(filePath);
		var contentType = 'text/html';
		switch (extname) {
			case '.js':
				contentType = 'text/javascript';
				break;
			case '.css':
				contentType = 'text/css';
				break;
		}
	
		var fullPath = path.join(root, filePath);
		path.exists(fullPath, function(exists) {
			if (exists) {
				fs.readFile(fullPath, function(error, content) {
					if (error) {
						response.writeHead(500);
						response.end();
					} else {
						response.writeHead(200, {
							'Content-Type' : contentType
						});
						response.end(content, 'utf-8');
					}
				});
			} else {
				console.log('not found "%s"', request.url);
				response.writeHead(404);
				response.end();
			}
		});
	
	});

  server.listen( PORT );
	
	console.log('Server running at http://127.0.0.1:' + PORT + '/');
}

main();

