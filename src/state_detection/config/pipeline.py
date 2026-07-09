class Pipeline:
    def __init__(self, steps):
        self.steps = steps
    def run_pipeline(self, df, *args):
        for func in self.steps:
            df = func(df, *args)

        return df
