# Daily Notes

## Day 1 Learning Note
Today, I explored the Django request lifecycle, tracing how a request flows from a web server through middleware to the view. The hands-on benchmark vividly showed the power of ASGI over WSGI. Running a simple app on Gunicorn (sync) resulted in a request pile-up under load, while Uvicorn (async) handled concurrent I/O-bound tasks effortlessly, maintaining low latency. This practical test clarified the huge performance gains of an asynchronous worker model for scalable applications. I also got a clear understanding of how middleware works via the __init__ (setup) and __call__ (per-request) methods.


## Day 2 Learning Note
🚀 Django Tip: URL Resolution Has a Price Tag (Albeit a Tiny One)

Ever wondered how Django translates a URL like /articles/123/ into the right view? Today, I dove into Django's URL resolving internals. The resolve() and reverse() functions are an elegant system for keeping code DRY and maintainable.

But the key insight? Performance.

I benchmarked a Django app with 5,000+ routes. The overhead to find the correct view, while incredibly small (under 1 millisecond), is real and measurable. This "resolution cost" is a great reminder that every layer of abstraction adds a tiny bit of latency. For 99% of apps, it's negligible. For hyperscale systems, those microseconds matter.

It's a perfect example of how understanding the internals helps in building not just functional, but truly scalable applications.



## Day 3 Learning Note (Detailed & Clear Version)
Django's Class-Based Views (CBVs) are like building with LEGOs 🧱. It's a simple idea, but it lets you create incredibly powerful and organized structures.

At first, a CBV seems like a roundabout way to handle a request, but breaking it down reveals its purpose.

The Foundation (.as_view()): A view class isn't a function, so it can't be plugged directly into Django's URL router. The .as_view() method is a clever factory that creates a tiny function on the fly. This function's only job is to create an instance of your view class every time a request comes in. This keeps the router simple and decouples it from your view's internal logic.

The Layers (Mixins & Inheritance): This is where the real power lies. Instead of writing one giant function with if statements for authentication, logging, and business logic, you can separate these concerns into "mixin" classes. Your final view then inherits from them.

An AuthenticationMixin only handles checking the user.

A LoggingMixin only handles logging the request.

Your MyView class only has to handle the core business logic.

The Connection (super()): The magic that holds these layers together is the super() function. When your AuthenticationMixin is done checking the user, it calls super().dispatch() to pass the request to the next layer in the chain (like the LoggingMixin). It's a predictable pipeline that keeps everything neat and in the right order. Python's Method Resolution Order (MRO) does this job neatly.

The big lesson here is reusability and separation of concerns. You can write an AuthenticationMixin once and then reuse that "LEGO brick" in dozens of different views. If you need to change your auth logic, you only change it in one place. This makes your code dramatically cleaner and easier to maintain.