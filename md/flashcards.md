Fiszki

What is REST?
    :wikipedia
    one way of providing interoperability between computer systems on the Internet. REST-compliant web services allow requesting systems to access and manipulate textual representations of web resources using a uniform and predefined set of stateless operations - usually HTTP verbs

What does REST stand for?
    Representational state transfer

Name two other forms of web service exist, beyond REST?
    :rest 
    WSDL, SOAP

What is a quine?
    :wikipedia
    A quine is a non-empty computer program which takes no input and produces a copy of its own source code as its only output.


Threads are expensive, and operating systems enforce a variety of hard caps on the number of threads a process, user, or machine may have. Give a ball park size of a thread
    50K

If we scale up to tens of thousands of simultaneous operations on concurrent sockets, which will run out first?
    threads, asyncio is the solution

C10K?
    Ten thousand connections, term coined by Kegel in 1999.

Create a nonblocking socket:
    sock = socket.socket()
    sock.setblocking(False)

Why does non blocking socket raise BlockingIOError on connect?
    A non-blocking socket throws an exception from connect, even when it is working normally. This exception replicates the irritating behavior of the underlying C function, which sets errno to EINPROGRESS to tell you it has begun.

What are two main features of async framework?
    non-blocking sockets and the event loop - to run concurrent operations on a single thread.

What's stack ripping?
    In async, it's the loss of context in a stack trace. The stack trace shows only that the event loop was running a callback. We do not remember what led to the error. The chain is broken on both ends: we forgot where we were going and whence we came. Stack ripping also prevents us from installing an exception handler for a chain of callbacks, the way a "try / except" block wraps a function call and its tree of descendents

What's a coroutine?
    it is a subroutine that can be paused and resumed. 

What's the rough size of a coroutine?
    3K   

> Wymień oktawy

Subkontra, Kontra, Wielka, Mała, Razkreślna, Dwukreślna, Trzykreślna...

> Wymień nuty oktawy małej

c, d, e, f, g, a, h 
