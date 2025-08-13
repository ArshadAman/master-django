# Daily Notes

## Day 1 Learning Note
Today, I explored the Django request lifecycle, tracing how a request flows from a web server through middleware to the view. The hands-on benchmark vividly showed the power of ASGI over WSGI. Running a simple app on Gunicorn (sync) resulted in a request pile-up under load, while Uvicorn (async) handled concurrent I/O-bound tasks effortlessly, maintaining low latency. This practical test clarified the huge performance gains of an asynchronous worker model for scalable applications. I also got a clear understanding of how middleware works via the __init__ (setup) and __call__ (per-request) methods.


## Day 2 Learning Note
🚀 Django Tip: URL Resolution Has a Price Tag (Albeit a Tiny One)

Ever wondered how Django translates a URL like /articles/123/ into the right view? Today, I dove into Django's URL resolving internals. The resolve() and reverse() functions are an elegant system for keeping code DRY and maintainable.

But the key insight? Performance.

I benchmarked a Django app with 5,000+ routes. The overhead to find the correct view, while incredibly small (under 1 millisecond), is real and measurable. This "resolution cost" is a great reminder that every layer of abstraction adds a tiny bit of latency. For 99% of apps, it's negligible. For hyperscale systems, those microseconds matter.

It's a perfect example of how understanding the internals helps in building not just functional, but truly scalable applications.