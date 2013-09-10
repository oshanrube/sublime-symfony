import sublime, sublime_plugin
import os
import os.path
import subprocess

class SymfonyCommand(sublime_plugin.TextCommand):
	base_directory = ''
	symfony_cmd = '';
	php_command = False
	def run(self, edit):
		#self.view.window().show_input_panel("Goto Line:", " hey how are ya ", self.on_done, None, None)
		found_root = self.loadRoot()
		if found_root:
			self.symfony_cmd = os.path.join(self.base_directory,'symfony');
			print "YEY found the symfony root"
			print self.symfony_cmd
		else:
			print "no luck"

	def loadRoot(self):
		view_name = self.view.file_name()
		dir_name = os.path.dirname(view_name)
		found_root = False
		reached_end = False
		while not found_root and not reached_end:
			for file in os.listdir(dir_name):
				if os.path.exists(os.path.join(dir_name,'symfony')) and os.path.isfile(os.path.join(dir_name,'symfony')):
					self.base_directory = dir_name
					found_root = True
			#comment
			old_dir = dir_name
			dir_name = os.path.dirname(dir_name)
			if dir_name == old_dir:
				reached_end = True
		if found_root:
			self.symfony_cmd = os.path.join(self.base_directory,'symfony');
			return True
		else:
			return False

	def callSymfony(self, command, quiet=False):
		self.loadRoot()
		if not self.symfony_cmd:
			if not quiet:
				return "Can't find the root directory of the symfony project."

		# CMD:
		if not self.php_command:
			command = "php "+self.symfony_cmd+" " + command
		else:
			command = self.php_command + "php "+self.symfony_cmd+"  --color " + command

		result, e = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=self.base_directory).communicate()
		if e:
			return e
		else:
			if not result and not quiet:
				result = "Finished " + command
			return result
	def output(self, value):
		self.multi_line_output(value)

	def multi_line_output(self, value, panel_name='SymfonyCommander'):
		# Create the output Panel
		panel = self.view.window().get_output_panel(panel_name)
		panel.set_read_only(False)
		panel.set_syntax_file('Packages/Text/Plain text.tmLanguage')
		edit = panel.begin_edit()
		panel.insert(edit, panel.size(), value)
		panel.end_edit(edit)
		panel.set_read_only(True)
		self.view.window().run_command("show_panel", {"panel": "output." + panel_name})

class SymfonyExecuteCommand(SymfonyCommand):
	def run(self, edit, command = ""):
		if command == "":
			self.view.window().show_input_panel("Command:", "", self.on_done, None, None)
		else:
			result = self.callSymfony(command)
			self.output(result);

	def on_done(self, text):
		result = self.callSymfony(text)
		self.output(result)

class SymfonyExecutePropelBuildSchemaCommand(SymfonyCommand):
	def run(self, edit, command = ""):
		if command == "":
			self.view.window().show_input_panel("Propel connection:", "", self.on_done, None, None)
		else:
			result = self.callSymfony("propel:build-schema --connection=\""+text+"\"")
			self.output(result)

	def on_done(self, text):
		result = self.callSymfony("propel:build-schema --connection=\""+text+"\"")
		self.output(result)

class SymfonyExecutePropelBuildClassesCommand(SymfonyCommand):
	def run(self, edit, command = ""):
		if command == "":
			self.view.window().show_input_panel("Propel connection:", "", self.on_done, None, None)
		else:
			result = self.callSymfony("propel:build --all-classes --connection=\""+text+"\"")
			self.output(result)

	def on_done(self, text):
		result = self.callSymfony("propel:build --all-classes --connection=\""+text+"\"")
		self.output(result)

class SymfonyExecutePublishAssertsCommand(SymfonyCommand):
	def run(self, edit):
		result = self.callSymfony("plugin:publish-assets")
		self.output(result)