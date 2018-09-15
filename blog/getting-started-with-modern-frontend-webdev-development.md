# 2017/01/01 - Getting Started With State of the Art Frontend Development

Nowdays I do a mix of Python system programming and Web UI
developements using Javascript (scss, backbone, classy, bootstrap).

I've diven a bit into state of the of the modern way of doing things,
prolly synonymous of state of the art. There is in my opinion three
main libraries that fight for the spotlight:

- Angular, which is basically a dead project
- React/Redux, the most popular solution, but
  it's very modular.
- Vue, is kind of inspired from react/redux,
  similarly it's very modular but the development
  is mostly centralized.

All three of them have a common point which is `diff`+`patch`
algorithms. That algorithm allows to declare the way the html should
look in its entierity and the algorithm make it happen in the
rendering graph by updating/remove/adding rendering nodes (which are
in the case of webdev, most of the time: DOM objects).

I kept that idea. I created bindings on top of snabbdom.js and
built what I could build, first getting inspiration from elm
and redux to come up with the most minimald and most versatile
framework for building web apps.

The canvas offered by this framework is summed by the following
`mount` procedure:

```scheme
(define (mount container init view)
  "Mount in node from the DOM named CONTAINER, the result of the state
returned by INIT passed to VIEW. VIEW must return pseudo sxml where
\"on-fu\" attributes (where fu is DOM event name) are associated with
action lambdas. An action looks like the following:

   (define (button-clicked state spawn)
     (lambda (event)
       (+ 1 state)))

In the above STATE is the current state. SPAWN allows to create
a new green thread. When the action returns the new state, the
VIEW procedure is called again with the new state.

A minimal VIEW procedure looks like the following:

   (define (view state)
     `(button (@ (on-click . ,button-clicked)) ,state))

A minimal INIT procedure looks like the following:

   (define (init) 1)

That's all folks!
"
  (let ((state (init)))  ;; init state
    ;; create a procedure that allows to create new green threads
    (letrec ((spawn (lambda (timeout proc args)
                      (set-timeout (lambda () (apply (proc state spawn) args)) timeout)))
             ;; lambda used to wrap event callback
             (make-action (lambda (action)
                            (lambda args
                              (let ((new (apply (action state spawn) args)))
                                (set! state new)
                                (render)))))
             ;; rendering pipeline
             (render (lambda ()
                       (set! container (patch container
                                              ((sxml->h* make-action) (view state)))))))
      (render))))
```

Basically, it says that `INIT` procedure produce a seed state
passed to `VIEW` which renders the first version of the graph
scene. A node from the graph scene fires an event, user specified
callbacks are which are called action procedures which basically
takes everything they need to:

- do ajax without blocking using an imperative syntax (via call/cc)
- spawn new green thread
- update the state

That's where will land the business code.

The `VIEW` procedure contains the UI code.

If you want to know more about this project head over
the [website](https://amirouche.github.io/forward.scm/) or have a look
at [this screencast on youtube](https://www.youtube.com/watch?v=aC0_Br9KWP4&list=PL_jCPpfzyfeqqEcioz71x5XvXnq9UABdK&index=7).
