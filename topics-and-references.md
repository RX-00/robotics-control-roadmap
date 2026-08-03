# Topics and References

<!-- roadmap-reference-index:start -->
This index mirrors the 59 topic nodes in the robot-control roadmap. Topic headings are synchronized from Draw.io; content beneath each heading is preserved.
<!-- roadmap-reference-index:end -->

<!-- roadmap-group:F -->
## 1. Mathematical and Computational Foundations

<!-- roadmap-topic:F1 -->
### Linear algebra and geometry

References:

- [Mathematics for Machine Learning](https://mml-book.github.io/) - Chapters 2-4, "Linear Algebra," "Analytic Geometry," and "Matrix Decompositions."

<!-- roadmap-topic:F2 -->
### Calculus and differential equations

References:

- [Mathematics for Machine Learning](https://mml-book.github.io/) - Chapter 5, "Vector Calculus."
- [MIT OpenCourseWare 18.03SC: Differential Equations](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/) - Units I-IV on first-order equations, second-order equations, Fourier/Laplace methods, and first-order systems.

<!-- roadmap-topic:F3 -->
### Probability, statistics, and stochastic processes

References:

- [Mathematics for Machine Learning](https://mml-book.github.io/) - Chapter 6, "Probability and Distributions."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 6, "Model Systems with Stochasticity," especially "The Master Equation," "Stationary Distributions," and "Finite Markov Decision Processes."

<!-- roadmap-topic:F4 -->
### Numerical methods and optimization

References:

- [Stanford EE364A: Convex Optimization I](https://see.stanford.edu/Course/EE364A) - Lectures 1-19, covering convex sets and functions, problem formulation, duality, approximation, statistical estimation, and interior-point methods.
- [Numerical Optimal Control](https://www.syscop.de/teaching/ss2020/numerical-optimal-control-online) - Lectures 2-8 on Newton-type methods, nonlinear optimization, constrained optimization, and derivative calculation.

<!-- roadmap-topic:F5 -->
### Signals, systems, and frequency response

References:

- [MIT OpenCourseWare 6.003: Signals and Systems](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/) - Lectures 1-11, especially continuous/discrete LTI systems, Fourier representations, frequency response, and Bode plots.

<!-- roadmap-topic:F6 -->
### Programming, algorithms, and real-time computing

References:

- [MIT OpenCourseWare 6.006: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) - Lectures and problem sets on algorithmic analysis, data structures, graph search, and dynamic programming.
- [CloudPendulum Onboarding](https://cloudpendulum.m2.chalmers.se/onboarding/) - Tutorials 3-5, "Do your first cloud experiment," "Implement your own control loop," and "VS Code Integration," for implementing and running control software against real hardware.

<!-- roadmap-group:M -->
## 2. Robot Modeling

<!-- roadmap-topic:M1 -->
### Coordinate frames, SO(3), and SE(3)

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Chapter 3, "Rigid-Body Motions," especially Sections 3.2-3.4 on rotation matrices, angular velocity, homogeneous transformations, twists, and wrenches.

<!-- roadmap-topic:M2 -->
### Forward and inverse kinematics

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Chapters 4 and 6, "Forward Kinematics" and "Inverse Kinematics."

<!-- roadmap-topic:M3 -->
### Jacobians, differential kinematics, and singularities

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Chapter 5, "Velocity Kinematics and Statics," especially Sections 5.1, 5.3, and 5.4 on Jacobians, singularities, and manipulability.

<!-- roadmap-topic:M4 -->
### Classical and analytical mechanics

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Appendix B, "Multi-Body Dynamics," especially "Deriving the equations of motion," "The Manipulator Equations," and "Variational mechanics."

<!-- roadmap-topic:M5 -->
### Rigid-body and multibody dynamics

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Chapter 8, "Dynamics of Open Chains."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Appendix B, "Multi-Body Dynamics," especially the manipulator equations and recursive dynamics algorithms.

<!-- roadmap-topic:M6 -->
### Constrained, contact, and hybrid dynamics

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 17, "Planning and Control through Contact," and Appendix B, "The Dynamics of Contact," including impulsive collision, time-stepping, and complementarity formulations.
- [MeMory of Motion Summer School Materials](https://memory-of-motion.github.io/summer-school/materials) - "Contact Models" lecture materials and associated Pinocchio tutorials.

<!-- roadmap-topic:M7 -->
### Continuous and discrete state-space models

References:

- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Chapter 2, "System Modeling," especially Section 2.2, "State Space Models," and Chapter 5, "Linear Systems."
- [Numerical Optimal Control](https://www.syscop.de/teaching/ss2020/numerical-optimal-control-online) - Lectures 9 and 14-15 on discrete-time optimal control, continuous-time optimal control, and numerical simulation.

<!-- roadmap-topic:M8 -->
### Sensors, actuators, friction, and transmissions

References:

- [MIT OpenCourseWare 2.12: Introduction to Robotics](https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/pages/lecture-notes/) - Chapter 2, "Actuators and Drive Systems."
- [MIT Robotic Manipulation](https://manipulation.mit.edu/) - Chapter 2, "Let's get you a robot," especially "Arms," "An aside: link dynamics with a transmission," "Sensors," and "Putting it all together."
- [CloudPendulum Onboarding](https://cloudpendulum.m2.chalmers.se/onboarding/) - Tutorials 3-4 on running a sensor-driven pendulum experiment and implementing a hardware control loop.

<!-- roadmap-topic:M9 -->
### Simulation, calibration, and system identification

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 18, "System Identification," especially parameter identification for mechanical systems, calibration, linear dynamical systems, neural models, and identification with contact.

<!-- roadmap-group:C -->
## 3A. Feedback and Control Theory

<!-- roadmap-topic:C1 -->
### Feedback, feedforward, and PID control

References:

- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Chapter 1, "Introduction," Chapter 10, "PID Control," and Section 11.2, "Feedforward Design."
- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Sections 11.1-11.2, "Control System Overview" and "Error Response."

<!-- roadmap-topic:C2 -->
### Transfer functions and frequency-domain control

References:

- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Chapters 8-9 and 11, "Transfer Functions," "Frequency Domain Analysis," and "Frequency Domain Design."

<!-- roadmap-topic:C3 -->
### Stability, Lyapunov theory, and passivity

References:

- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Chapter 4, especially Sections 4.3-4.4, "Stability" and "Lyapunov Stability Analysis."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 9, "Lyapunov Analysis," including Lyapunov functions, invariance, regions of attraction, robustness, and control-Lyapunov functions.
- [Nagoya University OpenCourseWare: Advanced Nonlinear Control](https://ocw.nagoya-u.jp/en/courses/0060-Advanced-Nonlinear-Control-2011/) - Lectures 1-7 on nonlinear-system stability, Lyapunov methods, input-output stability, and passivity.

<!-- roadmap-topic:C4 -->
### Controllability and observability

References:

- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Section 6.1, "Reachability," and Section 7.1, "Observability."

<!-- roadmap-topic:C5 -->
### Linear state-space control

References:

- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Chapters 5-7, "Linear Systems," "State Feedback," and "Output Feedback."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 8, "Linear Quadratic Regulators," including finite-horizon, time-varying, tracking, constrained, and manifold variants.

<!-- roadmap-topic:C6 -->
### Nonlinear and geometric control

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 3 sections "Partial feedback linearization" and "Swing-up control," plus Chapter 9, "Lyapunov Analysis."
- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Chapters 3 and 11 for Lie-group rigid-body representations and nonlinear robot motion control.
- [University of Illinois ECE 557: Geometric Control](https://publish.illinois.edu/geometric-control/) - Course material on control systems on manifolds, Lie groups, nonlinear controllability, nonholonomic/mechanical systems, and feedback linearization.

<!-- roadmap-topic:C7 -->
### Robust and adaptive control

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 13, "Robust and Stochastic Control," especially worst-case control, H-infinity control, structured uncertainty, adaptive control, and LPV control.
- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Chapter 12, "Robust Performance."

<!-- roadmap-group:E -->
## 3B. State Estimation

<!-- roadmap-topic:E1 -->
### Bayesian state estimation

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 19, "State Estimation," especially "Recursive Bayesian Filters."
- [Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/) by Thrun, Burgard, and Fox - Chapters 2-4 on recursive state estimation, Gaussian filters, and nonparametric filters.

<!-- roadmap-topic:E2 -->
### Observers and Kalman filtering

References:

- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Sections 7.2-7.4, "State Estimation," "Control Using Estimated State," and "Kalman Filtering."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 19 section "Observers and the Kalman Filter."

<!-- roadmap-topic:E3 -->
### EKF, UKF, and particle filtering

References:

- [Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/) by Thrun, Burgard, and Fox - Chapters 3-4, "Gaussian Filters" and "Nonparametric Filters."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 19 section "Recursive Bayesian Filters," including unscented Kalman and particle filters.

<!-- roadmap-topic:E4 -->
### Smoothing and factor graphs

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 19 section "Smoothing."
- [UCSD ECE276A: Sensing and Estimation in Robotics](https://natanaso.github.io/ece276a/schedule.html) - Lectures on factor-graph SLAM, Bayes filters, and smoothing.

<!-- roadmap-topic:E5 -->
### Sensor fusion, localization, and SLAM

References:

- [Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/) by Thrun, Burgard, and Fox - Chapters 5-11 on motion and sensor models, localization, mapping, FastSLAM, and GraphSLAM.
- [UCSD ECE276A: Sensing and Estimation in Robotics](https://natanaso.github.io/ece276a/schedule.html) - Lectures on motion/observation models, localization, odometry, factor-graph SLAM, and Bayes filtering.

<!-- roadmap-group:P -->
## 3C. Motion Planning

<!-- roadmap-topic:P1 -->
### Configuration spaces and collision checking

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Chapter 2, "Configuration Space," and Chapter 10, "Motion Planning."
- [Planning Algorithms](https://lavalle.pl/planning/web.html) by Steven M. LaValle - Chapters 3-5 on geometric representations, configuration spaces, collision detection, and sampling-based motion planning.

<!-- roadmap-topic:P2 -->
### Graph search and sampling-based planning

References:

- [Planning Algorithms](https://lavalle.pl/planning/web.html) by Steven M. LaValle - Chapter 2, "Discrete Planning," and Chapter 5, "Sampling-Based Motion Planning."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 12, "Sampling-based motion planning," including incremental search, PRMs, and RRTs.

<!-- roadmap-topic:P3 -->
### Kinodynamic and belief-space planning

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 12 section "RRTs for robots with dynamics" and Chapter 14, "Feedback Motion Planning."
- [Planning Algorithms](https://lavalle.pl/planning/web.html) by Steven M. LaValle - Chapters 9-12 on decision-theoretic planning, sequential decision theory, information spaces, and planning under sensing uncertainty.

<!-- roadmap-topic:P4 -->
### Trajectory generation and time scaling

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Chapter 9, "Trajectory Generation," including point-to-point trajectories, time scaling, and time-optimal time scaling.

<!-- roadmap-topic:P5 -->
### Trajectory optimization

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 10, "Trajectory Optimization," especially direct transcription, direct shooting, direct collocation, and practical solution techniques.
- [Numerical Optimal Control](https://www.syscop.de/teaching/ss2020/numerical-optimal-control-online) - Lecture 18, "Direct Approaches."

<!-- roadmap-group:O -->
## 3D. Optimal Control

<!-- roadmap-topic:O1 -->
### Calculus of variations and Pontryagin principle

References:

- [Numerical Optimal Control](https://www.syscop.de/teaching/ss2020/numerical-optimal-control-online) - Lectures 14 and 17, "Continuous time optimal control" and "Pontryagin and the indirect approach."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 10 section "Pontryagin's Minimum Principle."

<!-- roadmap-topic:O2 -->
### Dynamic programming and Hamilton-Jacobi theory

References:

- [Numerical Optimal Control](https://www.syscop.de/teaching/ss2020/numerical-optimal-control-online) - Lectures 11-12 and 16 on dynamic programming and the Hamilton-Jacobi-Bellman equation.
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 7, "Dynamic Programming," including continuous dynamic programming and the HJB equation.

<!-- roadmap-topic:O3 -->
### LQR, iLQR, and DDP

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 8, "Linear Quadratic Regulators," and Chapter 10 section "Iterative LQR and Differential Dynamic Programming."
- [Numerical Optimal Control](https://www.syscop.de/teaching/ss2020/numerical-optimal-control-online) - Lecture 13, "Differential Dynamic Programming."

<!-- roadmap-topic:O4 -->
### Constrained and stochastic optimal control

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 13, "Robust and Stochastic Control," especially costs and constraints for stochastic systems, stochastic LQR/MPC, and risk metrics.
- [Numerical Optimal Control](https://www.syscop.de/teaching/ss2020/numerical-optimal-control-online) - Lectures 6-7 on equality/inequality constrained optimization and Lectures 9-18 on optimal-control formulations.

<!-- roadmap-topic:O5 -->
### Linear, nonlinear, robust, and stochastic MPC

References:

- [UC Berkeley MPC Course Material](https://sites.google.com/berkeley.edu/mpc-lab/mpc-course-material) - Borrelli, Bemporad, and Morari, *Predictive Control for Linear and Hybrid Systems*, including stability, feasibility, robustness, explicit MPC, and real-time implementation.
- [Numerical Optimal Control](https://www.syscop.de/teaching/ss2020/numerical-optimal-control-online) - Lecture 19, "Model predictive control."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 10 section "Model-Predictive Control" and Chapter 13 sections on stochastic and robust MPC.

<!-- roadmap-group:R -->
## 4. Contact-Rich Robot and Whole-Body Control

<!-- roadmap-topic:R1 -->
### Joint-space tracking and actuator control

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Sections 11.2 and 11.4, "Error Response" and "Motion Control with Torque or Force Inputs," including joint-space PID and feedforward control.

<!-- roadmap-topic:R2 -->
### Computed torque and inverse-dynamics control

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Section 11.4, "Motion Control with Torque or Force Inputs," especially the computed-torque controller and computed-torque plus feedforward control.

<!-- roadmap-topic:R3 -->
### Task-space and operational-space control

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 3 section "Task-space partial feedback linearization."
- [MeMory of Motion Summer School Materials](https://memory-of-motion.github.io/summer-school/materials) - TSID lecture slides and notebooks on task-space inverse dynamics.

<!-- roadmap-topic:R4 -->
### Redundancy resolution and null-space control

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Sections 5.3-5.4, "Singularities" and "Manipulability," and Chapter 6, "Inverse Kinematics," for Jacobian pseudoinverses and redundant inverse kinematics.
- [MIT Robotic Manipulation](https://manipulation.mit.edu/) - Chapter 3 sections "Differential inverse kinematics" and "Differential inverse kinematics with constraints," including the Jacobian pseudoinverse and joint-centering objectives.
- [Intelligent Robot Control lectures](https://cobotat.ijs.si/lectures/) - Lectures 3-4, "Control of Redundant Robots" and "Control of Redundant Robots Multiple Tasks."

<!-- roadmap-topic:R5 -->
### Force, impedance, and admittance control

References:

- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Sections 11.5-11.6, "Force Control" and "Hybrid Motion-Force Control."
- [MIT Robotic Manipulation](https://manipulation.mit.edu/) - Chapter 8, "Manipulator Control," especially direct/indirect force control, hybrid position-force control, and joint/Cartesian stiffness control.
- [Intelligent Robot Control lectures](https://cobotat.ijs.si/lectures/) - Lectures 5-7 on force, impedance, and admittance control.

<!-- roadmap-topic:R6 -->
### Whole-body control and hierarchical QPs

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 5 section "Whole-Body Control," following the centroidal-dynamics and whole-body-planning sections.
- [MeMory of Motion Summer School Materials](https://memory-of-motion.github.io/summer-school/materials) - TSID lecture slides, tutorials, and notebooks on joint-space and task-space inverse-dynamics control formulated as constrained optimization.

<!-- roadmap-topic:R7 -->
### Contact scheduling, grasping, and locomotion control

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapters 4-5 and 17, "Simple Models of Walking and Running," "Highly-articulated Legged Robots," and "Planning and Control through Contact."
- [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) - Chapter 12, "Grasping and Manipulation," including contact kinematics, friction, form closure, and force closure.

<!-- roadmap-group:L -->
## 5. Learning and Learning-Based Control

<!-- roadmap-topic:L1 -->
### Supervised learning and function approximation

References:

- [Understanding Deep Learning](https://udlbook.github.io/udlbook/) - Chapters 2-7, covering supervised learning, shallow/deep networks, loss functions, model fitting, and gradient computation.
- [MIT 6.S191: Introduction to Deep Learning](https://introtodeeplearning.com/) - Lecture 1, "Intro to Deep Learning," and Software Lab 1, "Deep Learning in Python."

<!-- roadmap-topic:L2 -->
### MDPs, POMDPs, and Bellman equations

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 6 section "Finite Markov Decision Processes," Chapter 7 on Bellman/HJB equations, and Chapter 15 section "Partially-observable Markov Decision Processes."

<!-- roadmap-topic:L3 -->
### Value iteration and policy iteration

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 7 sections on numerical value iteration and Chapter 11 section "Policy Iteration."
- [UC Berkeley CS 285: Deep Reinforcement Learning](https://rail.eecs.berkeley.edu/deeprlcourse-fa23/) - Lectures 7-8, "Value Function Methods" and "Deep RL with Q-Functions."

<!-- roadmap-topic:L4 -->
### Imitation and inverse reinforcement learning

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 21, "Imitation Learning," including behavior cloning, distribution shift, visuomotor policies, and inverse reinforcement learning.
- [UC Berkeley CS 285: Deep Reinforcement Learning](https://rail.eecs.berkeley.edu/deeprlcourse-fa23/) - Lecture 2, "Supervised Learning of Behaviors," and Lecture 20, "Inverse Reinforcement Learning."

<!-- roadmap-topic:L5 -->
### Reinforcement learning

References:

- [MIT 6.S191: Introduction to Deep Learning](https://introtodeeplearning.com/) - Lecture 5, "Deep Reinforcement Learning."
- [Understanding Deep Learning](https://udlbook.github.io/udlbook/) - Chapter 19, "Deep Reinforcement Learning."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 20, "Model-Free Policy Search."

<!-- roadmap-topic:L6 -->
### Learned dynamics, representations, and residual models

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 18 sections "Learning models for control," "Residual physics models with linear function approximators," and "Neural network models."
- [Understanding Deep Learning](https://udlbook.github.io/udlbook/) - Chapters 11-14 on residual networks, transformers, graph neural networks, and unsupervised representation learning.

<!-- roadmap-topic:L7 -->
### Model-based, model-free, and offline RL

References:

- [UC Berkeley CS 285: Deep Reinforcement Learning](https://rail.eecs.berkeley.edu/deeprlcourse-fa23/) - Lectures 4-9 on model-free RL, Lectures 11-12 on model-based RL, and Lectures 15-16 on offline RL.

<!-- roadmap-topic:L8 -->
### Hybrid learning and model-based control

References:

- [Synthesis of Model Predictive Control and Reinforcement Learning: Survey and Classification](https://arxiv.org/abs/2502.02133) by Reiter et al. - Survey of the shared foundations, complementary strengths, and major architectures for combining MPC with reinforcement learning.
- [UC Berkeley CS 285: Deep Reinforcement Learning](https://rail.eecs.berkeley.edu/deeprlcourse-fa23/) - Lectures 10-12, "Optimal Control and Planning," "Model-Based Reinforcement Learning," and "Model-Based Policy Learning."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapters 10, 18, and 20 for trajectory optimization/MPC, learned control models, and model-free policy search.

<!-- roadmap-group:D -->
## 6. Safety and Real-World Deployment

<!-- roadmap-topic:D1 -->
### Constraints, saturation, and anti-windup

References:

- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Sections 10.4-10.5, "Integrator Windup" and "Implementation."
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 1 section "Input and State Constraints."

<!-- roadmap-topic:D2 -->
### Uncertainty, robustness, and risk

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 13, "Robust and Stochastic Control," including stochastic models, worst-case control, model uncertainty, H-infinity control, domain randomization, and alternative risk metrics.
- [Feedback Systems](https://authors.library.caltech.edu/records/yzs24-xsx88) by Astrom and Murray - Chapter 12, "Robust Performance."

<!-- roadmap-topic:D3 -->
### CLFs, CBFs, reachability, and safety filters

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 9 sections "Barrier functions," "Finite-time Reachability," and "Control-Lyapunov Functions."

<!-- roadmap-topic:D4 -->
### Real-time optimization, latency, and embedded control

References:

- [UC Berkeley MPC Course Material](https://sites.google.com/berkeley.edu/mpc-lab/mpc-course-material) - *Predictive Control for Linear and Hybrid Systems*, particularly the material on explicit MPC and real-time implementation.
- [CloudPendulum Onboarding](https://cloudpendulum.m2.chalmers.se/onboarding/) - Tutorial 4, "Implement your own control loop," for executing a custom controller against remote real-time hardware.

<!-- roadmap-topic:D5 -->
### Sim-to-real, domain randomization, and adaptation

References:

- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 13 section "Domain randomization" and Chapter 18 sections on online estimation and adaptive control.
- [UC Berkeley CS 285: Deep Reinforcement Learning](https://rail.eecs.berkeley.edu/deeprlcourse-fa23/) - Lecture 22, "Meta-Learning and Transfer Learning."

<!-- roadmap-topic:D6 -->
### Verification, hardware-in-the-loop, and experiments

References:

- [CloudPendulum Onboarding](https://cloudpendulum.m2.chalmers.se/onboarding/) - Tutorials 3, 7, and 8 on simulation/hardware experiments, repeatable disturbances, and controller benchmarking.
- [Underactuated Robotics](https://underactuated.csail.mit.edu/) - Chapter 9, "Lyapunov Analysis," for computational verification of stability, regions of attraction, robustness, and reachability.

<!-- roadmap-topic:D7 -->
### Deployment-ready robot autonomy

References:

- [CloudPendulum Onboarding](https://cloudpendulum.m2.chalmers.se/onboarding/) - Tutorials 3-8 provide an end-to-end progression from simulation and hardware control loops through Gymnasium integration, disturbances, and benchmarking on real hardware.
- [MeMory of Motion Summer School Materials](https://memory-of-motion.github.io/summer-school/materials) - Lecture and tutorial materials on Pinocchio, TSID, contact models, numerical optimal control, and Crocoddyl.
