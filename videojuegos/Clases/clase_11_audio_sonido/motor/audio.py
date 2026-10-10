import pygame


class AudioManager:
    """
    Gestor centralizado para cargar y reproducir música y efectos de sonido.
    """

    def __init__(self, num_channels=16):
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(num_channels)
            self.sounds = {}
            self.music_path = None
            print("AudioManager inicializado correctamente.")
        except pygame.error as e:
            print(f"Error al inicializar AudioManager: {e}. El audio estará desactivado.")
            self.sounds = None  # Desactivamos el audio si hay error

    def load_sound(self, name, path):
        """Carga un efecto de sonido y lo asocia con un nombre clave."""
        if self.sounds is None: return
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Error al cargar el sonido '{name}' desde '{path}': {e}")

    def play_sound(self, name, loops=0):
        """Reproduce un sonido por su nombre en el primer canal disponible."""
        if self.sounds is None or name not in self.sounds:
            return

        # Busca un canal que no esté ocupado para reproducir el sonido
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sounds[name], loops)

    def load_music(self, path):
        """Carga la ruta para la música de fondo."""
        if self.sounds is None: return
        self.music_path = path

    def play_music(self, loops=-1, volume=0.5):
        """Reproduce la música de fondo."""
        if self.sounds is None or not self.music_path:
            return
        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
        except pygame.error as e:
            print(f"Error al reproducir la música desde '{self.music_path}': {e}")

    def stop_music(self):
        if self.sounds is None: return
        pygame.mixer.music.stop()