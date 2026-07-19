@property
def is_on(self):
    return any(
        warning.wtype == self.entity_description.warning_type
        for warning in self.warnings
    )
