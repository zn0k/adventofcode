from collections import deque

class IntCode():
    def __init__(self, 
        program=None, 
        input_file=None, 
        debug=False, 
        input_values=[], 
        live_output=False,
        single_step_output=False):
        self.PARAM = 0
        self.WRITER = 1
        self.cursor = 0
        self.debug = debug
        self.input_values = deque(input_values)
        self.output_values = deque()
        self.live_output = live_output
        self.param_modes = None
        self.single_step_output = single_step_output
        self.terminated = False
        self.relative_base = 0
        self.op = 99

        if program == None and input_file == None:
            raise Exception("Must provide either a parsed program or a file")
        if input_file:
            with open(input_file, "r") as f:
                line = f.readlines()[0]
                self.program = [int(op) for op in line.rstrip().split(",")]
        if program:
            self.program = program

    def _get(self, index):
        if index < 0:
            raise Exception("Invalid memory access at register {index}")
        if index >= len(self.program):
            self.program += [0] * (index - len(self.program) + 1)
        return self.program[index]

    def _set(self, index, value):
        if index < 0:
            raise Exception("Invalid memory access at register {index}")
        if index >= len(self.program):
            self.program += [0] * (index - len(self.program) + 1)
        self.program[index] = value

    def _get_params(self, hints=[]):
        params = []
        for i in range(0, len(hints)):
            param_cursor = self.cursor + 1 + i
            #if hints[i] == self.WRITER:
            #    params.append(self._get(param_cursor))
            #else:
            if self.param_modes[i] == 0:
                params.append(self._get(self._get(param_cursor)))
            elif self.param_modes[i] == 1:
                params.append(self._get(param_cursor))
            elif self.param_modes[i] == 2:
                params.append(self._get(self.relative_base + self._get(param_cursor)))
        if self.debug: 
            print(f"_get_params for op {self.op} at cursor {self.cursor} with hints {hints} and modes {self.param_modes} returning parameters {params}")
        return params

    def _new_cursor(self, params):
        new_cursor = self.cursor + len(params) + 1
        if self.debug:
            print(f"_new_cursor returning {new_cursor}")
        return new_cursor

    def run(self, input_values=[]):
        if input_values:
            self.input_values = deque(input_values)
        while self.op:
            op = str(self._get(self.cursor)).zfill(5)
            self.param_modes = list(reversed([int(c) for c in op[0:3]]))
            self.op = int(op[3::])
            if self.op == 99:
                if self.debug:
                    print(f"terminating with opcode 99 at {self.cursor}")
                self.terminated = True
                if self.output_values:
                    return self.output_values
                else:
                    return self.program
            func = getattr(self, f"_op{self.op}")
            self.cursor = func()
            if self.op == 4 and self.single_step_output:
                return self.output_values[-1]

    def _op1(self):
        params = [self.PARAM, self.PARAM, self.WRITER]
        x, y, dest = self._get_params(params)
        self._set(dest, x + y)
        if self.debug:
            print(f"_op1 wrote {x + y} to {dest}")
        return self._new_cursor(params)

    def _op2(self):
        params = [self.PARAM, self.PARAM, self.WRITER]
        x, y, dest = self._get_params(params)
        self._set(dest, x * y)
        if self.debug:
            print(f"_op2 wrote {x * y} to {dest}")
        return self._new_cursor(params)

    def _op3(self):
        params = [self.WRITER]
        dest = self._get_params(params)[0]
        if len(self.input_values):
            input_value = self.input_values.popleft()
        else:
            input_value = int(input("Input value: "))
        self._set(dest, input_value)
        if self.debug:
            print(f"_op3 wrote input value {input_value} to {dest}")
        return self._new_cursor(params)

    def _op4(self):
        params = [self.PARAM]
        val = self._get_params(params)[0]
        if self.live_output:
            print(f"Output: {val}")
        self.output_values.append(val)
        if self.debug:
            print(f"_op4 output value {val}")
        return self._new_cursor(params)

    def _op5(self):
        params = [self.PARAM, self.PARAM]
        val, cursor = self._get_params(params)
        if val != 0: 
            return cursor
        else:
            return self._new_cursor(params)

    def _op6(self):
        params = [self.PARAM, self.PARAM]
        val, cursor = self._get_params(params)
        if val == 0: 
            return cursor
        else:
            return self._new_cursor(params)

    def _op7(self):
        params = [self.PARAM, self.PARAM, self.WRITER]
        op1, op2, dest = self._get_params(params)
        self._set(dest, 1 if op1 < op2 else 0)
        return self._new_cursor(params)

    def _op8(self):
        params = [self.PARAM, self.PARAM, self.WRITER]
        op1, op2, dest = self._get_params(params)
        self._set(dest, 1 if op1 == op2 else 0)
        return self._new_cursor(params)

    def _op9(self):
        params = [self.PARAM]
        offset = self._get_params(params)[0]
        self.relative_base += offset
        return self._new_cursor(params)