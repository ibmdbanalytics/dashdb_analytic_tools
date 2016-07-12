def bundle(handler, absolute_notebook_path):
  '''
  Transforms, converts, bundles, etc. the notebook. Then issues a Tornado web 
  response using the handler to redirect the browser, download a file, show
  an HTML page, etc. This function must finish the handler response before
  returning either explicitly or by raising an exception.

  :param handler: The tornado.web.RequestHandler that serviced the request
  :param absolute_notebook_path: The path of the notebook on disk
  '''
  handler.finish('Hello world!')
