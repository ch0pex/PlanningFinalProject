;; Fifteen puzzle problem:
;; Hard1 is one of the "hardest" instances of the puzzle,
;; i.e., having one of the longest solutions.

;; Esta versión usa diferentes conjuntos de objetos para las coordenadas x e y.

(define (problem hard1-15)
  (:domain strips-sliding-tile)
  (:objects 
    t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15 
    x1 x2 x3 x4 
    y1 y2 y3 y4)
  (:init
    ;; Definición de tipos
    (tile t1) (tile t2) (tile t3) (tile t4) (tile t5)
    (tile t6) (tile t7) (tile t8) (tile t9) (tile t10)
    (tile t11) (tile t12) (tile t13) (tile t14) (tile t15)
    
    (position x1) (position x2) (position x3) (position x4)
    (position y1) (position y2) (position y3) (position y4)
    
    ;; Relaciones de adyacencia en coordenadas x
    (inc x1 x2) (inc x2 x3) (inc x3 x4)
    (dec x4 x3) (dec x3 x2) (dec x2 x1)
    
    ;; Relaciones de adyacencia en coordenadas y
    (inc y1 y2) (inc y2 y3) (inc y3 y4)
    (dec y4 y3) (dec y3 y2) (dec y2 y1)
    
    ;; Posición inicial del espacio en blanco
    (blank x1 y1)
    
    ;; Posiciones iniciales de las fichas
    (at t1 x2 y1)  (at t2 x3 y1)  (at t3 x4 y1)
    (at t4 x1 y2)  (at t5 x2 y2)  (at t6 x3 y2)  (at t7 x4 y2)
    (at t8 x1 y3)  (at t9 x2 y3)  (at t10 x3 y3) (at t11 x4 y3)
    (at t12 x1 y4) (at t13 x2 y4) (at t14 x3 y4) (at t15 x4 y4)
  )
  (:goal
    (and 
      ;; Definir la configuración objetivo de las fichas
      (at t15 x1 y1) (at t14 x2 y1) (at t13 x3 y1) (at t12 x4 y1)
      (at t11 x1 y2) (at t10 x2 y2) (at t9 x3 y2)  (at t8 x4 y2)
      (at t7 x1 y3)  (at t6 x2 y3)  (at t5 x3 y3)  (at t4 x4 y3)
      (at t3 x1 y4)  (at t2 x2 y4)  (at t1 x3 y4)  (blank x4 y4)
    )
  )
)
