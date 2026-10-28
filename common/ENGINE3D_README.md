# engine3d cheat sheet
Import: `from common.engine3d import *`. Scene class: `class X(Stage3D)`; start with `self.setup_stage("iso")`.
Colors: black/white only; `ACCENT` (blue) ONLY to show change (firing, selection, result).
Views: iso flat top side front back34 low high. `self.view(name, run)`, `tour([..])`, `orbit()`, `dolly()`, `spin()`.
2D content inside a 3D scene: use `self.view("flat", 0.01)`; normal Tex/MathTex/ImageMobject work there.
Objects: box cylinder sphere cone torus arrow3d segment axes3d grid_floor curve3d voxels cnn_stack
Surfaces: surface bowl_surface saddle_surface gaussian_surface
Data: scatter_classes plane_poly bars3d matrix_grid grid_cell
Nets: Net3D(layers).reveal/forward_pass/fire_layer/reset/fade ; Perceptron3D(n_in).reveal/fire/reset/fade
Stage: caption label3d reveal keep clear_scene blue unblue pulse signal
Never wrap DashedLine inside DashedVMobject. Only smooth/rush_into/rush_from/linear rate functions.

# engine3d_ml cheat sheet (from common.engine3d_ml import *)
Helpers: lit(m) / unlit(m) (blue on/off), tags(scene,[(text,pos)]), flashes(scene,[(a,b)])
CNN: ConvSweep(n,k).reveal/sweep/reset ; PoolDemo().reveal/pool ; CNN3D(spec).reveal/forward/reset
Sequence: RNNUnrolled3D(steps).reveal/run/reset ; LSTMCell3D().reveal/fire/reset ; Attention3D(n).reveal/focus/unfocus/sweep
Training: CompGraph3D.linear_loss().reveal/forward/backward/reset ; LossLandscape().reveal/descend(lr,steps,momentum,dashed)
          gradient_arrow(fn,p) ; Autoencoder3D().reveal/squeeze ; dropout/undrop(scene,net,layer,idx) ; backprop(scene,net)
          ResBlock3D().reveal/fire/reset
Classic: sigmoid_surface boundary_line blobs2d ; KMeans3D().reveal/step(i) ; SVMMargin3D().reveal/show_margin/highlight_support
         DecisionTree3D().reveal/fire_path/reset ; embedding_cloud + show_neighbors ; batch_stack
All reveal() calls auto-register objects, so scene.clear_scene() removes them.
