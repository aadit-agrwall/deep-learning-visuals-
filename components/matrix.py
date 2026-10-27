from manim import *


class Matrix2D(VGroup):
    """
    Reusable Matrix Component

    Features (V1 Part 1)
    --------------------
    • Any matrix size
    • Integer / float support
    • Automatic spacing
    • Scalable brackets
    • Uses MobjectMatrix internally
    """

    def __init__(
        self,
        data,
        color=WHITE,
        bracket_color=WHITE,
        number_color=WHITE,
        scale_factor=0.8,
        decimal_places=2,
        h_buff=1.2,
        v_buff=0.9,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._validate(data)

        self.data = [row[:] for row in data]

        self.rows = len(data)
        self.cols = len(data[0])

        self.color = color
        self.number_color = number_color
        self.bracket_color = bracket_color

        self.scale_factor = scale_factor
        self.decimal_places = decimal_places

        self.h_buff = h_buff
        self.v_buff = v_buff

        self.entries = []
        self.original_colors = []

        self._build_matrix()

        self.add(self.matrix)

    # ---------------------------------------------------
    # Validation
    # ---------------------------------------------------

    def _validate(self, data):

        if not isinstance(data, (list, tuple)):
            raise TypeError("Matrix must be a list of lists.")

        if len(data) == 0:
            raise ValueError("Matrix cannot be empty.")

        cols = len(data[0])

        for row in data:

            if len(row) != cols:
                raise ValueError("Every row must have same length.")

            for value in row:
                if not isinstance(value, (int, float)):
                    raise TypeError(
                        "Matrix entries must be int or float."
                    )

    # ---------------------------------------------------
    # Build Matrix
    # ---------------------------------------------------

    def _build_matrix(self):

        values = []

        for row in self.data:

            new_row = []

            for value in row:

                number = DecimalNumber(
                    value,
                    num_decimal_places=self.decimal_places,
                    color=self.number_color,
                )

                number.scale(self.scale_factor)

                new_row.append(number)

            values.append(new_row)

        self.matrix = MobjectMatrix(
            values,
            h_buff=self.h_buff,
            v_buff=self.v_buff,
            left_bracket="[",
            right_bracket="]",
        )

        self.matrix.get_brackets().set_color(
            self.bracket_color
        )

        self.entries = values

        self.original_colors = [
            [self.number_color for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    # ---------------------------------------------------
    # Helpers
    # ---------------------------------------------------

    def get_entry(self, row, col):

        return self.entries[row][col]

    def get_row(self, row):

        return self.entries[row]

    def get_column(self, col):

        return [
            self.entries[r][col]
            for r in range(self.rows)
        ]

    def get_entries(self):

        return self.entries

    def get_brackets(self):

        return self.matrix.get_brackets()

    def get_data(self):

        return [row[:] for row in self.data]

    # ---------------------------------------------------
    # Animation
    # ---------------------------------------------------

    def create_animation(self):

        return AnimationGroup(

            FadeIn(self.matrix.get_entries()),

            Create(self.matrix.get_brackets()),

            lag_ratio=0.15

        )
    def highlight_element(
      self,
      row,
      col,
      color=YELLOW,
    ):
      return self.entries[row][col].animate.set_color(color)


    def highlight_row(
       self,
       row,
       color=BLUE,
    ):
       return AnimationGroup(
        *[
            entry.animate.set_color(color)
            for entry in self.entries[row]
        ],
        lag_ratio=0.1,
        )


    def highlight_column(
      self,
      col,
      color=GREEN,
    ):
      return AnimationGroup(
        *[
            self.entries[r][col]
            .animate
            .set_color(color)
            for r in range(self.rows)
        ],
        lag_ratio=0.1,
      )


    def highlight(
      self,
      color=YELLOW,
    ):
      return AnimationGroup(
        *[
            entry.animate.set_color(color)
            for row in self.entries
            for entry in row
         ]
      )



    def reset(self):

     animations = []

     for row in self.entries:
        for entry in row:
            animations.append(
                entry.animate.set_color(
                    self.number_color
                )
            )

     animations.append(
        self.matrix.get_brackets()
        .animate
        .set_color(self.bracket_color)
     )

     return AnimationGroup(*animations)


    def update_value(self, row, col, value):

        old = self.entries[row][col]

        new = DecimalNumber(
           value,
           num_decimal_places=self.decimal_places,
           color=self.number_color,
        )

        new.scale(self.scale_factor)
        new.move_to(old)

        self.entries[row][col] = new
        self.data[row][col] = value

        return ReplacementTransform(old, new)



    def swap_rows(
        self,
        r1,
        r2,
    ):

      animations = []

      for c in range(self.cols):

        a = self.entries[r1][c]
        b = self.entries[r2][c]

        pos = a.get_center()

        animations.append(
            a.animate.move_to(
                b.get_center()
            )
        )

        animations.append(
            b.animate.move_to(pos)
        )

        self.entries[r1][c], self.entries[r2][c] = (
            self.entries[r2][c],
            self.entries[r1][c],
        )

        self.data[r1][c], self.data[r2][c] = (
            self.data[r2][c],
            self.data[r1][c],
        )

      return AnimationGroup(*animations)




    def swap_columns(
        self,
        c1,
        c2,
    ):

     animations = []

     for r in range(self.rows):

        a = self.entries[r][c1]
        b = self.entries[r][c2]

        pos = a.get_center()

        animations.append(
            a.animate.move_to(
                b.get_center()
            )
        )

        animations.append(
            b.animate.move_to(pos)
        )

        self.entries[r][c1], self.entries[r][c2] = (
            self.entries[r][c2],
            self.entries[r][c1],
        )

        self.data[r][c1], self.data[r][c2] = (
            self.data[r][c2],
            self.data[r][c1],
        )

     return AnimationGroup(*animations)



    def copy_matrix(self):
     return Matrix2D(
        self.get_data(),
        color=self.color,
        bracket_color=self.bracket_color,
        number_color=self.number_color,
        scale_factor=self.scale_factor,
        decimal_places=self.decimal_places,
        h_buff=self.h_buff,
        v_buff=self.v_buff,
     )



    