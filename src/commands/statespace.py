import numpy
from wpilib import Timer, Notifier
from wpilib.command import Command

from subsystems import Drivetrain


class StateSpaceController:
    def __init__(self, A, Ainv, B, C, D, K, Kff, L):
        self.A = A
        self.Ainv = Ainv
        self.B = B
        self.C = C
        self.D = D
        self.K = K
        self.Kff = Kff
        self.L = L
        self.u_min = -12
        self.u_max = 12
        self.u = numpy.zeros((self.B.shape[1], 1))
        self.y = numpy.zeros((self.C.shape[0], 1))
        self.r = numpy.zeros((self.A.shape[0], 1))
        self.x_hat = numpy.zeros((self.A.shape[0], 1))
        self.reset()

    def reset(self):
        self.u = numpy.zeros((self.B.shape[1], 1))
        self.y = numpy.zeros((self.C.shape[0], 1))
        self.r = numpy.zeros((self.A.shape[0], 1))
        self.x_hat = numpy.zeros((self.A.shape[0], 1))

    default_r = numpy.zeros(shape=(1,1))

    def update_input(self, next_r=default_r):
        self.u = self.K @ (self.r - self.x_hat)
        if next_r is not self.default_r:
            uff = self.Kff @ (next_r  - self.A @ self.r)
            self.r = next_r
        else:
            uff = self.Kff @ (self.r - self.A @ self.r)
        self.u = numpy.clip(self.u + uff, self.u_min, self.u_max)

    def predict(self):
        self.x_hat = self.A @ self.x_hat + self.B @ self.u

    def correct(self):
        self.x_hat += self.Ainv @ self.L @ (self.y - self.C @ self.x_hat - self.D @ self.u)

    def check_shape(self, matrix_name, shape):
        m = getattr(self, matrix_name)
        assert m.shape == shape, "%s shape expected %s, was %s" % (matrix_name, shape, m.shape)


class StateSpaceDriveController(StateSpaceController):
    def __init__(self, drivetrain: Drivetrain):
        """
        x: (left position (m), left velocity (m/s), right position (m), right velocity (m/s).T
        y: (left position (m), right position (m)).T

        :param drivetrain:
        """
        from numpy import array as matrix
        derpymodel = False
        if derpymodel:
            A = matrix([[1., 0.01694108, 0., 0.00250869],
                        [0., 0.72295618, 0., 0.22253044],
                        [0., 0.00250869, 1., 0.01694108],
                        [0., 0.22253044, 0., 0.72295618]])

            B = matrix([[0.00108648, -0.00083504],
                        [0.09866299, -0.07375227],
                        [-0.00083504, 0.00108648],
                        [-0.07375227, 0.09866299]])

            C = matrix([[1, 0, 0, 0],
                        [0, 0, 1, 0]])

            D = matrix([[0., 0.],
                        [0., 0.]])

            K = matrix([[60.90638737, 7.93224841, 21.38859796, 5.13312445],
                        [21.38859796, 5.13312445, 60.90638737, 7.93224841]])

            Kff = matrix([[706.64972496, 1.70156933, 289.74584796, 0.76636392],
                          [289.74584796, 0.76636392, 706.64972496, 1.70156933]])

            L = matrix([[1.16232192, 0.11368756],
                        [7.55194606, 5.86548273],
                        [0.11368756, 1.16232192],
                        [5.86548273, 7.55194606]])

            Ainv = matrix([[1., -0.0247057, 0., 0.00413452],
                           [0., 1.52797747, 0., -0.47032104],
                           [0., 0.00413452, 1., -0.0247057],
                           [0., -0.47032104, 0., 1.52797747]])
        else:
            A = matrix([[1., 0.01631643, 0., 0.00238268],
                        [0., 0.66737266, 0., 0.20542149],
                        [0., 0.00238268, 1., 0.01631643],
                        [0., 0.20542149, 0., 0.66737266]])

            B = matrix([[0.00123499, -0.00079884],
                        [0.11152021, -0.06887181],
                        [-0.00079884, 0.00123499],
                        [-0.06887181, 0.11152021]])

            C = matrix([[1, 0, 0, 0],
                        [0, 0, 1, 0]])

            D = matrix([[0, 0],
                        [0, 0]])

            K = matrix([[56.82612189, 6.03969859, 18.60045886, 3.51953103],
                        [18.60045886, 3.51953103, 56.82612189, 6.03969859]])

            Kff = matrix([[731.26285269, 1.74253981, 334.3110478, 0.86234499],
                          [334.3110478, 0.86234499, 731.26285269, 1.74253981]])

            L = matrix([[1.12809912, 0.08747579],
                        [5.70458841, 4.3576656],
                        [0.08747579, 1.12809912],
                        [4.3576656, 5.70458841]])

            Ainv = matrix([[1., -0.02579361, 0., 0.0043692],
                           [0., 1.65523823, 0., -0.5094927],
                           [0., 0.0043692, 1., -0.02579361],
                           [0., -0.5094927, 0., 1.65523823]])
        super().__init__( A=A, Ainv=Ainv, B=B, C=C, D=D, K=K, Kff=Kff, L=L )
        self.drivetrain = drivetrain
        self.period = Command.getRobot().getPeriod()
        self._at_reference = False

    def make_reference_m(self, left_pos_m, left_vel_mps, right_pos_m, right_vel_mps):
        return numpy.array([[left_pos_m, left_vel_mps, right_pos_m, right_vel_mps]]).T

    def make_reference_ft(self, left_pos_ft, right_pos_ft, left_vel_fps, right_vel_fps):
        return self.make_reference_m(left_pos_ft, right_pos_ft, left_vel_fps, right_vel_fps) / 3.28

    def update(self, left_pos_m, right_pos_m, left_vel_mps, right_vel_mps):
        self.check_shape("A", (4,4))
        self.check_shape("B", (4,2))
        self.check_shape("C", (2,4))
        self.check_shape("D", (2,2))
        self.check_shape("r", (4,1))
        self.check_shape("x_hat", (4,1))
        self.check_shape("y", (2,1))
        self.check_shape("u", (2,1))
        self.check_shape("Kff", (2,4))
        self.check_shape("K", (2,4))
        self.check_shape("L", (4,2))
        self.correct()
        self.update_input(self.make_reference_m(left_pos_m, left_vel_mps, right_pos_m, right_vel_mps))
        self._send_input()
        self.update_measurements()
        self.predict()

    def _send_input(self):
        voltage = self.drivetrain.getVoltage()
        vpl = self.u[0,0] / voltage
        vpr =-self.u[1,0] / voltage
        self.drivetrain.setLeftMotor(vpl)
        self.drivetrain.setRightMotor(vpr)

    def update_measurements(self):
        pos_l_ft = self.drivetrain.getLeftEncoder() / self.drivetrain.ratio
        pos_r_ft =-self.drivetrain.getRightEncoder() / self.drivetrain.ratio
        self.y[0,0] = pos_l_ft / 3.28 # meter
        self.y[1,0] = pos_r_ft / 3.28 # meter


