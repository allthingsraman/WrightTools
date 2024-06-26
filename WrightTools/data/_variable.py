"""Variable class and associated."""

# --- import --------------------------------------------------------------------------------------


import h5py

from .._dataset import Dataset

__all__ = ["Variable"]


# --- class ---------------------------------------------------------------------------------------


class Variable(Dataset):
    """Variable."""

    class_name = "Variable"

    def __init__(self, parent, id, units=None, **kwargs):
        """Variable.

        Parameters
        ----------
        parent : WrightTools.Data
            Parent data object.
        id : h5py DatasetID
            Dataset ID.
        units : string (optional)
            Variable units. Default is None.
        kwargs
            Additional keys and values to be written into dataset attrs.
        """
        self._parent = parent
        super().__init__(id)
        if units is not None:
            self.units = units
        # attrs
        if self._parent.file.mode is not None and self._parent.file.mode != "r":
            self.attrs.update(kwargs)
            self.attrs["name"] = h5py.h5i.get_name(self.id).decode().split("/")[-1]
            self.attrs["class"] = self.class_name

    @property
    def label(self) -> str:
        return self.attrs.get("label", "")

    @label.setter
    def label(self, label):
        self.attrs["label"] = label

    def _to_dict(self):
        out = {}
        out["name"] = self.natural_name
        out["values"] = self[:]
        out["units"] = self.units
        out["label"] = self.label
        out.update(self.attrs)
        return out
