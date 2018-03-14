import kivy
import threading
from kivy.clock import Clock
import World
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle

kivy.require('1.10.0')


class GridLabelCellHolder(GridLayout):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.set_layout()

    def on_size(self, *args):
        self.canvas.before.clear()

        if self.id is "cliff":
            with self.canvas.before:
                # Color(249 / 255, 6 / 255, 6 / 255, 1)
                Rectangle(pos=self.pos, size=self.size, source='red_cell.jpeg')
        if self.id is "goal":
            with self.canvas.before:
                Color(50 / 255, 205 / 255, 50 / 255, 1)
                Rectangle(pos=self.pos, size=self.size, source='start_cell.jpg')
        if self.id is "start":
            with self.canvas.before:
                Color(0 / 255, 140 / 255, 165 / 255, 1)
                Rectangle(pos=self.pos, size=self.size, source='start_cell.jpg')
        if self.id is "normal":
            with self.canvas.before:
                Color(119 / 255, 115 / 255, 115 / 255, 1)
                Rectangle(pos=self.pos, size=self.size, source='blue_cell.jpeg')

    def set_layout(self):

        if self.id is "cliff":
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(text="c (-100)"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(id="buffer"))

        if self.id is "goal":
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(text="50"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(id="buffer"))

        if self.id is "start" or self.id is "normal":
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(text=" ", id="qval_top"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(text=" ", id="qval_left"))
            if self.id is "start":
                self.add_widget(Button(id="Agent", background_normal='', background_color=[248 / 255, 255 / 255, 0, 1]))
            else:
                self.add_widget(Button(id="agentPlaceholder", background_normal='', background_color=[0, 0, 0, 0]))

            self.add_widget(Label(text=" ", id="qval_right"))
            self.add_widget(Label(id="buffer"))
            self.add_widget(Label(text=" ", id="qval_bottom"))

    def update_qval(self, direction, new_value):

        if self.id is "normal" or self.id is "start":
            for qvalue in self.children:
                if "top" in qvalue.id and direction is 1:
                    qvalue.text = new_value
                if "left" in qvalue.id and direction is 2:
                    qvalue.text = new_value
                if "right" in qvalue.id and direction is 3:
                    qvalue.text = new_value
                if "bottom" in qvalue.id and direction is 4:
                    qvalue.text = new_value

    def reset_qvals(self):

        if self.id is "normal" or self.id is "start":
            for qval in self.children:
                if "qval" in qval.id:
                    qval.text = " "


class GameGridApp(App):

    def __init__(self, c, r, **kwargs):
        super().__init__(**kwargs)
        self.grid = GridLayout(cols=c, rows=r, spacing=2)
        self.window_container = BoxLayout(orientation="vertical")
        self.config = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, 0.08))
        self.display = BoxLayout(id="display", orientation="horizontal", spacing=10, size_hint=(1, 0.08))
        self.is_playing = None
        self.time_delay = 0.5
        self.current_cell = None
        self.generationField = None
        self.scoreField = None
        self.exploreField = None
        self.deathField = None
        self.algoTypeField = None
        self.world = World.World(c, r)
        self.start_dropdown = DropDown()
        self.prepare_config()
        self.prepare_display()
        self.load_info_to_grid()
        self.load_windows()

    def prepare_config(self):

        pre = TextInput(id="pre",
                        hint_text="Pretraining...",
                        multiline=False,
                        input_filter="int",
                        background_color=[0 / 255, 203 / 255, 255 / 255, 0.5])
        self.config.add_widget(pre)

        alpha = TextInput(id="alpha",
                          hint_text="α value (=0.2)",
                          multiline=False,
                          input_filter="float",
                          background_color=[0 / 255, 203 / 255, 255 / 255, 0.5])
        self.config.add_widget(alpha)
        self.config.add_widget(Button(text="set α",
                                      background_color=[0 / 255, 203 / 255, 255 / 255, 0.5],
                                      on_press=lambda x: self.adjust_alpha(alpha.text)))

        epsilon = TextInput(id="explore",
                            hint_text="ε value (=0.1)",
                            multiline=False,
                            input_filter="float",
                            background_color=[0 / 255, 203 / 255, 255 / 255, 0.5])
        self.config.add_widget(epsilon)
        self.config.add_widget(Button(text="set ε",
                                      background_color=[0 / 255, 203 / 255, 255 / 255, 0.5],
                                      on_press=lambda x: self.adjust_epsilon(epsilon.text)))

        gamma = TextInput(id="gamma",
                          hint_text="γ value (=0.9)",
                          multiline=False,
                          input_filter="float",
                          background_color=[0 / 255, 203 / 255, 255 / 255, 0.5])
        self.config.add_widget(gamma)
        self.config.add_widget(Button(text="set γ",
                                      background_color=[0 / 255, 203 / 255, 255 / 255, 0.5],
                                      on_press=lambda x: self.adjust_gamma(gamma.text)
                                      ))

        choose = self.build_dropdown()
        self.config.add_widget(choose)

        self.config.add_widget(Button(text="START",
                                      background_normal='',
                                      background_color=[0 / 255, 140 / 255, 165 / 255, 1],
                                      on_press=lambda a: self.reset_and_start(choose.text,
                                                                              pre.text,
                                                                              epsilon.text,
                                                                              alpha.text,
                                                                              gamma.text)))

        self.config.add_widget(Button(text="PLAY/PAUSE",
                                      background_normal="",
                                      background_color=[0 / 255, 140 / 255, 165 / 255, 1],
                                      on_press=lambda a: self.pause_resume()))


    def adjust_gamma(self,text):
        if text is not "":
            self.world.agent.ai.gamma = float(text)
            print(self.world.agent.ai.gamma)

    def adjust_alpha(self,text):
        if text is not "":
            self.world.agent.ai.alpha = float(text)

    def adjust_epsilon(self,text):
        if text is not "":
            self.world.agent.ai.epsilon = float(text)
            print(self.world.agent.ai.epsilon)

    def build_dropdown(self):


        sarsa = Button(text="sarsa",
                       height=22,
                       size_hint_y=None,
                       background_normal='',
                       background_color=[0 / 255, 140 / 255, 165 / 255, 1]
                       )

        sarsa.bind(on_release=lambda btn: self.start_dropdown.select(sarsa.text))

        self.start_dropdown.add_widget(sarsa)

        qlearn = Button(text="qlearn",
                        height=22,
                        size_hint_y=None,
                        background_normal='',
                        background_color=[0 / 255, 140 / 255, 165 / 255, 1]
                        )
        qlearn.bind(on_release=lambda btn: self.start_dropdown.select(qlearn.text))

        self.start_dropdown.add_widget(qlearn)

        choose_button = Button(text="Choose",
                               background_normal='',
                               background_color=[0 / 255, 140 / 255, 165 / 255, 1])

        choose_button.bind(on_release=self.start_dropdown.open)
        self.start_dropdown.bind(on_select=lambda instance, x: setattr(choose_button, 'text', x))

        return choose_button

    def prepare_display(self):
        self.display.add_widget(Label(text="algo"))
        self.algoTypeField = TextInput(id="AlgoType",
                                       readonly=True, text="",
                                       multiline=False,
                                       background_color=[0 / 255, 203 / 255, 255 / 255, 0.5])
        self.display.add_widget(self.algoTypeField)

        self.display.add_widget(Label(text="gen"))
        self.generationField = TextInput(id="generation",
                                         readonly=True,
                                         text="0",
                                         multiline=False,
                                         background_color=[0 / 255, 203 / 255, 255 / 255, 0.5])
        self.display.add_widget(self.generationField)

        self.display.add_widget(Label(text="score"))
        self.scoreField = TextInput(id="score",
                                    readonly=True,
                                    text="0",
                                    multiline=False,
                                    background_color=[0 / 255, 203 / 255, 255 / 255, 0.5])
        self.display.add_widget(self.scoreField)

        self.display.add_widget(Label(text="deaths"))
        self.deathField = TextInput(id="deaths",
                                    readonly=True,
                                    text="0",
                                    multiline=False,
                                    background_color=[0 / 255, 203 / 255, 255 / 255, 0.5])
        self.display.add_widget(self.deathField)

        self.display.add_widget(Label(text="explore"))
        self.exploreField = (TextInput(id="explore",
                                       readonly=True,
                                       text="0",
                                       multiline=False,
                                       background_color=[0 / 255, 203 / 255, 255 / 255, 0.5]))
        self.display.add_widget(self.exploreField)

    def load_windows(self):
        self.window_container.add_widget(self.config)
        self.window_container.add_widget(self.display)
        self.window_container.add_widget(self.grid)

    def reset_and_start(self, agent_type, pretraining, epsilon, alpha, gamma):
        eps = 0.1
        al = 0.2
        ga = 0.9
        pre = 0
        if epsilon is not "":
            eps = float(epsilon)
        if alpha is not "":
            al = float(alpha)
        if gamma is not "":
            ga = float(gamma)
        if pretraining is not "":
            pre = int(pretraining)

        if agent_type is not "Choose":
            if self.is_playing is not None:
                self.is_playing.cancel()
            self.generationField.text = "0"
            self.deathField.text = "0"
            self.exploreField.text = "0"
            self.algoTypeField.text = agent_type
            self.reset_all_qvals()
            self.world.add_agent(agent_type, eps, al, ga)
            self.world.do_pretraining(pre)
            if pre is not 0:
                self.set_agent_pos(self.world.agent.cell.name)
            self.generationField.text = str(pre)
            self.update_all_qvals()
            threading.Thread(target=self.do_the_loop()).start()

    def update_display(self):
        self.deathField.text = str(self.world.agent.deaths)
        self.scoreField.text = str(self.world.agent.score)
        self.exploreField.text = str(self.world.agent.ai.explore)

    def update_callback(self, dt):
        new_cell_name = self.world.agent.update_status()
        self.set_agent_pos(new_cell_name)
        self.update_generation()
        self.update_display()
        self.update_all_qvals()

    def update_generation(self):
        gen_int = int(self.generationField.text)
        gen_int += 1
        self.generationField.text = str(gen_int)

    def pause_resume(self):
        if self.algoTypeField.text is not "":
            if self.is_playing is None:
                self.do_the_loop()
            else:
                self.is_playing.cancel()
                self.is_playing = None

    def do_the_loop(self):

        self.is_playing = Clock.schedule_interval(self.update_callback, self.time_delay)

    def update_all_qvals(self):
        for key, value, in self.world.agent.ai.qvalues:
            qval = str(self.world.agent.ai.qvalues[key, value])
            if len(qval) > 6:
                qval = qval[:6]+".."
            cell = self.find_cell(key)
            action = value
            cell.update_qval(action, qval)

    def reset_all_qvals(self):
        for cell in self.grid.children:
            cell.reset_qvals()

    def find_cell(self, cellname):
        for cell in self.grid.children:
            if cell.name is cellname:
                return cell
        return None

    def set_agent_pos(self, newcellname):

        for agentvalue in self.current_cell.children:

            if agentvalue.id is "Agent":
                agentvalue.id = "agentPlaceholder"
                agentvalue.background_color = [0, 0, 0, 0]

        for cell in self.grid.children:

            if cell.name is newcellname:

                self.current_cell = cell

                for agentvalue in cell.children:

                    if agentvalue.id is "agentPlaceholder":
                        agentvalue.id = "Agent"
                        agentvalue.background_color = [248 / 255, 255 / 255, 0, 1]




    def load_info_to_grid(self):

        self.world.build_gamegrid()

        for cell in self.world.gamegrid:

            cell_id = None

            if cell.start:
                cell_id = "start"
            if cell.goal:
                cell_id = "goal"
            if cell.cliff:
                cell_id = "cliff"
            if cell.field:
                cell_id = "normal"

            grid_cell = GridLabelCellHolder(cell.name, id=cell_id, cols=3, rows=3)

            if cell.start:
                self.current_cell = grid_cell

            self.grid.add_widget(grid_cell)

    def build(self):
        return self.window_container


