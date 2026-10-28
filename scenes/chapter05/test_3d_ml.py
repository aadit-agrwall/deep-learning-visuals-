from manim import *
import numpy as np
from common.engine3d import *
from common.engine3d_ml import *


class Test3DML(Stage3D):
    def construct(self):
        self.setup_stage("iso")
        report = []

        def log(line):
            report.append(line)
            open("/tmp/engine3d_ml_test.txt", "w").write("\n".join(report) + "\n")

        def shot(name, fn):
            try:
                self.view("iso", 0.3)
                fn(); log("OK    " + name)
            except Exception as e:
                log(f"FAIL  {name}: {type(e).__name__}: {e}")
                try:
                    self.remove(*self.mobjects)
                except Exception:
                    pass
                self._stage = []; self._cap = None

        def conv():
            self.caption("Convolution")
            c = ConvSweep(); c.reveal(self); self.view("top", 1.0)
            c.sweep(self, 0.12); self.clear_scene()

        def pool():
            self.caption("Max pooling")
            p = PoolDemo(); p.reveal(self); self.view("top", 1.0)
            p.pool(self, 0.5); self.clear_scene()

        def cnn():
            self.caption("CNN forward pass")
            n = CNN3D(); n.reveal(self); n.forward(self, 0.5); n.reset(self)
            self.view("front", 1.0); self.clear_scene()

        def rnn():
            self.caption("RNN unrolled")
            r = RNNUnrolled3D(3); r.reveal(self); r.run(self, 0.4); r.reset(self); self.clear_scene()

        def lstm():
            self.caption("LSTM cell")
            l = LSTMCell3D(); l.reveal(self); self.view("front", 1.0)
            l.fire(self, 0.4); l.reset(self); self.clear_scene()

        def attention():
            self.caption("Attention")
            a = Attention3D(4); a.reveal(self); a.sweep(self, rows=[0, 2]); self.clear_scene()

        def graph():
            self.caption("Computation graph")
            g = CompGraph3D.linear_loss(); g.reveal(self); self.view("front", 1.0)
            g.forward(self, 0.4); g.reset(self); g.backward(self, 0.4); g.reset(self)
            self.clear_scene()

        def boundary():
            self.caption("Logistic regression")
            ax = axes3d(); surf = sigmoid_surface()
            self.reveal(ax, surf, anim="create", run=1.2)
            line = boundary_line((1.2, 0.8), 0); pos, neg, pp, nn = blobs2d()
            self.reveal(pos, neg, line, run=0.8)
            self.view("top", 1.2); self.clear_scene()

        def landscape():
            self.caption("Gradient descent")
            ls = LossLandscape(); ls.reveal(self)
            ls.descend(self, steps=6, step_run=0.25)
            ls.descend(self, start=(-2.0, 1.5), steps=6, momentum=0.5, step_run=0.25, dashed=True)
            ga = gradient_arrow(ls.fn, (1.0, -1.5)); self.reveal(ga, run=0.6)
            self.view("top", 1.2); self.clear_scene()

        def autoenc():
            self.caption("Autoencoder, dropout, backprop")
            ae = Autoencoder3D(); ae.reveal(self, 2.0); ae.squeeze(self); ae.reset(self)
            dropout(self, ae, 1, [0, 2]); undrop(self, ae, 1, [0, 2])
            backprop(self, ae, 0.4); ae.reset(self); self.clear_scene()

        def resblock():
            self.caption("Residual block")
            rb = ResBlock3D(); rb.reveal(self); self.view("front", 1.0)
            rb.fire(self, 0.4); rb.reset(self); self.clear_scene()

        def kmeans():
            self.caption("k-means")
            km = KMeans3D(); km.reveal(self)
            for i in range(min(2, len(km.steps))):
                km.step(self, i, 0.8)
            self.clear_scene()

        def svm():
            self.caption("SVM margin")
            s = SVMMargin3D(); s.reveal(self); s.show_margin(self); s.highlight_support(self)
            self.view("side", 1.2); self.clear_scene()

        def tree():
            self.caption("Decision tree")
            t = DecisionTree3D(); t.reveal(self); self.view("front", 1.0)
            t.fire_path(self, (0, 1, 0), 0.4); t.reset(self); self.clear_scene()

        def embed():
            self.caption("Embeddings and batches")
            grp, pts = embedding_cloud(); self.reveal(grp, run=1.0)
            show_neighbors(self, grp, pts, 0, 3); self.clear_scene(0.5)
            bs = batch_stack(); self.reveal(bs, run=0.8); self.clear_scene()

        shot("ConvSweep", conv)
        shot("PoolDemo", pool)
        shot("CNN3D", cnn)
        shot("RNNUnrolled3D", rnn)
        shot("LSTMCell3D", lstm)
        shot("Attention3D", attention)
        shot("CompGraph3D forward/backward", graph)
        shot("sigmoid surface + boundary + blobs", boundary)
        shot("LossLandscape + gradient_arrow", landscape)
        shot("Autoencoder3D + dropout + backprop", autoenc)
        shot("ResBlock3D", resblock)
        shot("KMeans3D", kmeans)
        shot("SVMMargin3D", svm)
        shot("DecisionTree3D", tree)
        shot("embedding_cloud + batch_stack", embed)
        self.wait(0.5)
