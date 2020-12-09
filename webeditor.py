"""
GPT-2-simple Web editor.
"""
import argparse
import time

import bottle

import gpt_2_simple as gpt2


class WebEditorServer(object):
    """
    Webserver for gpt-2 completion.
    """
    def __init__(self, runname, modelname):
        self.runname = runname
        self.modelname = modelname
        
        # initialize session
        print("Preparing GPT-2...")
        self.session = gpt2.start_tf_sess()
        gpt2.load_gpt2(self.session)
        print("Done.")
        
        # create server
        self.server = bottle.Bottle()
        
        # bind addresses
        self.server.get("/", callback=self.get_mainpage)
        self.server.get("/style.css", callback=self.get_style)
        self.server.get("/completion.py", callback=self.get_completion_script)
        self.server.get("/complete", callback=self.get_complete)
    
    def get_mainpage(self):
        """
        Serve the mainpage.
        """
        return """
        <HTML>
            <HEAD>
                <meta charset="utf-8">
                <TITLE>GPT-2 Web Editor</TITLE>
                <link rel="stylesheet" href="/style.css"></link>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/brython/3.8.10/brython.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/brython/3.8.10/brython_stdlib.min.js"></script>
            </HEAD>
            <BODY onload="brython()">
                <script type="text/python" src="/completion.py"></script>
                <DIV class="container">
                    <DIV class="half" id="inputdiv">
                        <TEXTAREA id="doc"></TEXTAREA>
                    </DIV>
                    <DIV class="half" id="outputdiv"></TEXTAREA>
                    </DIV>
                </DIV>
            </BODY>
        </HTML>
        """
    
    def get_completion_script(self):
        """
        Serve the completion script.
        """
        return r"""
        from browser import document, markdown, ajax
        
        def complete(text):
            # complete the text
            document["doc"].disabled = True
            ajax.get("/complete", data={"text": text}, oncomplete=on_complete_response)
        
        def on_complete_response(req):
            # called on complete() response
            document["doc"].value += req.text
            document["doc"].disabled = False
            update_markdown()
            
        
        def keydown(evt):
            prevent = False
            # check if we should complete
            if evt.keyCode == 9:
                complete(document["doc"].value)
                prevent = True
            
            if prevent:
                # prevent further execution
                evt.preventDefault()
                return False
            return True
        
        def update_markdown(evt):
            # update the rendered markdown
            text = document["doc"].value
            markdowned, scripts = markdown.mark(text)
            document["outputdiv"].html = markdowned
        
        def main():
            # the main function
            # bind events
            textarea = document["doc"]
            textarea.bind("keydown", keydown)
            textarea.bind("keyup", update_markdown)
        
        main()
        """
    
    def get_style(self):
        """
        Serve the style file.
        """
        return """
        .container {
            display: flex;
            height: 100%;
            width: 100%;
        }
        
        .half {
            height:100%;
            border: 1px solid black;
            
        }
        
        .half:first-of-type {
            width:50%;
        }
        
        .half:not(:first-of-type){
            flex-grow: 1;
        }
        
        textarea {
            width: 100%;
            height: 100%;
        }
        """
    
    def get_complete(self):
        """
        Complete some text.
        """
        text = bottle.request.params.get("text", "")
        prefix = text
        
        gpt2results = gpt2.generate(
            self.session,
            model_name=self.modelname,
            run_name=self.runname,
            prefix=prefix,
            return_as_list=True,
            seed=int(time.time()),
            temperature=0.8,
            top_k=50,
            top_p=0.9,
            nsamples=1,
            )
        
        completed = gpt2results[0][len(prefix):]
        return completed
        
    
    def run(self, host, port):
        """
        Start the server.
        """
        self.server.run(interface=host, port=port)


def main():
    """
    The main function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store", type=int, help="port to serve on", default=8080)
    parser.add_argument("-i", "--interface", action="store", help="interface to serve on", default="0.0.0.0")
    parser.add_argument("--model", action="store", default="124M", help="model to use")
    parser.add_argument("--run-name", action="store", dest="runname", default="run1", help="run name of the finetuned model.")
    ns =  parser.parse_args()
    
    server = WebEditorServer(ns.runname, ns.model)
    server.run(host=ns.interface, port=ns.port)

if __name__ == "__main__":
    main()
