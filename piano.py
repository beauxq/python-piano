import pygame, numpy, pygame.sndarray
from collections import defaultdict


class Piano:
    def __init__(self, transpose=0):
        self.sample_rate = 44100
        pygame.mixer.pre_init(self.sample_rate, -16, 1)
        pygame.init()
        self.transpose = transpose

        self.notes = {
            pygame.K_n: self.make_note(self.get_freq(0)),  # A 440
            pygame.K_h: self.make_note(self.get_freq(-1)),  # down
            pygame.K_b: self.make_note(self.get_freq(-2)),
            pygame.K_g: self.make_note(self.get_freq(-3)),
            pygame.K_v: self.make_note(self.get_freq(-4)),
            pygame.K_c: self.make_note(self.get_freq(-5)),
            pygame.K_d: self.make_note(self.get_freq(-6)),
            pygame.K_x: self.make_note(self.get_freq(-7)),
            pygame.K_s: self.make_note(self.get_freq(-8)),
            pygame.K_z: self.make_note(self.get_freq(-9)),  # C below A 440
            pygame.K_j: self.make_note(self.get_freq(1)),  # Bb above A 440
            pygame.K_m: self.make_note(self.get_freq(2)),  # B

            pygame.K_q: self.make_note(self.get_freq(3)),  # C above A 440
            pygame.K_2: self.make_note(self.get_freq(4)),
            pygame.K_w: self.make_note(self.get_freq(5)),
            pygame.K_3: self.make_note(self.get_freq(6)),
            pygame.K_e: self.make_note(self.get_freq(7)),
            pygame.K_r: self.make_note(self.get_freq(8)),
            pygame.K_5: self.make_note(self.get_freq(9)),
            pygame.K_t: self.make_note(self.get_freq(10)),
            pygame.K_6: self.make_note(self.get_freq(11)),
            pygame.K_y: self.make_note(self.get_freq(12)),
            pygame.K_7: self.make_note(self.get_freq(13)),
            pygame.K_u: self.make_note(self.get_freq(14)),

            pygame.K_i: self.make_note(self.get_freq(15)),
            pygame.K_9: self.make_note(self.get_freq(16)),
            pygame.K_o: self.make_note(self.get_freq(17)),
            pygame.K_0: self.make_note(self.get_freq(18)),
            pygame.K_p: self.make_note(self.get_freq(19)),
            pygame.K_LEFTBRACKET: self.make_note(self.get_freq(20)),
            pygame.K_EQUALS: self.make_note(self.get_freq(21)),
            pygame.K_RIGHTBRACKET: self.make_note(self.get_freq(22)),
            pygame.K_BACKSPACE: self.make_note(self.get_freq(23)),
            # keyboard layouts differ in what key is beside right bracket
            pygame.K_BACKSLASH: self.make_note(self.get_freq(24)),
            pygame.K_RETURN: self.make_note(self.get_freq(24))
        }

        self.keys = defaultdict(lambda: False)

        self.screen = pygame.display.set_mode((150, 50))
        pygame.display.set_caption('Piano')

        self.clock = pygame.time.Clock()
        done = False
        while not done:
            self.clock.tick(180)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    self.keys = defaultdict(lambda: False)
                elif event.type == pygame.KEYDOWN:
                    self.keys[event.key] = True
                    if event.key in self.notes:
                        self.notes[event.key].set_volume(1)
                        self.notes[event.key].play(-1)
                elif event.type == pygame.KEYUP:
                    self.keys[event.key] = False
                    if event.key in self.notes:
                        self.notes[event.key].fadeout(200)
            for key, sound in self.notes.items():
                if self.keys[key]:
                    vol = sound.get_volume()
                    if vol > 0.5:
                        sound.set_volume(vol - 0.00390625)  # 1/256

    def get_freq(self, h):
        """ h is half steps away from A 440
        transpose will also be added """
        return 440.0 * 2 ** ((self.transpose + h) / 12)

    def make_note(self, freq):
        """ sin wave
        amplitude 4096 / max signed 16 bit int
        1 wavelength at the given frequency (to be repeated)

        frequencies are ceilinged to a fraction of the sample rate
        A 440.00 -> 44100/100 = 441
        C 261.63 -> 44100/168 = 262.5
        """
        return pygame.sndarray.make_sound(numpy.array(
            [4096 * numpy.sin(2.0 * numpy.pi * freq * x / self.sample_rate)
             for x in range(0, int(self.sample_rate / freq))]
        ).astype(numpy.int16))


def main():
    Piano()

if __name__ == "__main__":
    main()
