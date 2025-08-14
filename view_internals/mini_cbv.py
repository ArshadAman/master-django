from django.http import HttpResponse

class LoggingMixin:
    """A mixin that logs when dispatch starts and finishes"""
    def dispatch(self, request, *args, **kwargs):
        print("--> Entering LoggingMixin.dispatch()")
        # Use super() to call the next dispatch in the MRO chain
        response = super().dispatch(request, *args, **kwargs)
        print("<-- Exiting LoggingMixin.dispatch()")
        return response
    
class MiniView:
    "A mini version of Django's View class"

    @classmethod
    def as_view(cls, **initkwargs):
        "A simplified version of as_view()"
        def view_function(request, *args, **kwargs):
            # Create instance of the clas
            self = cls(**initkwargs)
            # call the instance's dispatch() method
            return self.dispatch(request, *args, **kwargs)
        return view_function
    
    def dispatch(self, request, *args, **kwargs):
        """A simplified dispatch() that also instruments MRO"""
        print("--> Entering MiniView.dispatch()")
        print("Method Resolution Order (MRO):")
        for i, c in enumerate(self.__class__.__mro__):
            print(f"   {i}:  {c.__name__}")

        handler_name = request.method.lower()
        handler = getattr(self, handler_name, self.http_method_not_allowed)
        print(f"Dispatching to handler: {handler_name}")
        response = handler(request, *args, **kwargs)
        print("<-- Exiting MiniView.dispatch()")
        return response
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello from MiniView's GET method")
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("Method Not Allowed", status=405)
        
class MyTestView(LoggingMixin, MiniView):
    pass
    """A test view combining our mixin and base view"""
    # def get(self, request, *args, **kwargs):
    #     print("--- Executing MyTestView's GET logic! ---")
    #     return HttpResponse("Hello from MyTestView's GET method!")
