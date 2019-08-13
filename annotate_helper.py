import re
import json
import spacy
from pathlib import Path
import uuid


class AnnotateHelper:

    def __init__(self, raw_text):
        """
        Assists in helping to annotate the text of a document.
        :param raw_text: str.  A string representation of the text for a document.
        """
        self.raw_text = raw_text

        self.entities = []

    def drop_entity(self, entity_id):
        """
        Removes an entity from the entity list.
        :param entity_id: Address and label of entity to remove.
        :return: Edits the self.entities list.
        """
        for entity in self.entities:
            if entity["id"] == entity_id:
                self.entities.remove(entity)
                print("The following entity was removed: ")
                print(entity)

    def suggest_entities(self, ner_model):
        """
        Applies an existing NER model to the document to suggest what entities are in the document.
        :param ner_model: Path to the NER model.
        :return: Returns a list of detected entities in the text.
        """
        nlp = spacy.load(ner_model)
        doc = nlp(self.raw_text)

        identified_entities = []
        for ent in doc.ents:
            entity_text = self.raw_text[ent.start_char:ent.end_char]
            entity = {
                "id": str(uuid.uuid4().hex),
                "text": entity_text,
                "start_idx": ent.start_char,
                "end_idx": ent.end_char,
                "label": ent.label_
            }
            print(entity["id"], entity["text"], entity["label"])
            self.entities.append(entity)

        return identified_entities

    def get_entity_span(self, phrase, match_case=True, label=None, context_len=30):
        """
        Searches the text for an occurrence of the specified entity.  For each occurrence of the text the context is
        printed and you are prompted if you want to add the text as an entity.
        :param phrase: str.  The phrase to search for.
        :param match_case: bool. (optional) Whether the matching should be case-sensitive.
        :param label: str. (optional) Name of the label to assign to the entity.  If set then the same label will be
            assigned to each occurrence of the phrase in the text.  Otherwise user will have the option to set the
            label manually.
        :param context_len: int.  Default=30.  Number of begin/end characters surrounding the phrase to include to
            determine context of the phrase.
        :return:
        """
        # Find all the matches for the phrase.
        if match_case:
            matches = list(re.finditer(phrase, self.raw_text))
        else:
            matches = list(re.finditer(phrase.lower(), self.raw_text.lower()))

        # Check if there are any matches in the text.
        if len(matches) == 0:
            print("There were no matches for the text provided.  Check spelling or try not matching on case.")
            return

        print("There were {} matching phrases in the text.\n".format(str(len(matches))))

        # Add the matching phrase locations to the entities list.
        for m in matches:
            start_idx = m.span()[0]
            end_idx = m.span()[1]

            entity = {
                "id": str(uuid.uuid4()),
                "text": phrase,
                "start_idx": start_idx,
                "end_idx": end_idx,
                "label": label
            }

            subset_start = start_idx - context_len

            if subset_start < 0:
                subset_start = 0

            subset_end = end_idx + context_len

            cred = '\033[91m'
            cend = '\033[0m'

            highlight_text = cred + self.raw_text[start_idx:end_idx] + cend

            print("".join([self.raw_text[subset_start:start_idx], highlight_text, self.raw_text[end_idx:subset_end]]))
            add_entity = input("Do you want to add this to your entity list? (y/n) ")

            if add_entity == "y":
                response = self.add_entity(entity)

                print(response)
            else:
                print("Okay let's try the next one...\n")

    def add_entity(self, entity):
        """
        Gathers information about an entity tag before adding it to the document entities list.
        :param entity: An entity object.
        """
        if entity["label"] is None:
            label = input("What should the label be for this entity? ")

            while label == '':
                print('Label cannot be an empty string')
                label = input("What should the label be for this entity? ")

            entity["label"] = label.upper()

        if entity in self.entities:
            return "Entity already exists.\n"
        else:
            self.entities.append(entity)
            return "ENTITY ADDED!\n"

    def view_annotated_document(self, focus_entity=None):
        """
        Print the document with entities marked by their colors.
        :param focus_entity: List of entities to focus on in the document.
        :return: Prints the document with entities color coded.
        """
        colors = [
            '\033[91m',
            '\033[96m',
            '\033[36m',
            '\033[94m',
            '\033[92m'
        ]

        if focus_entity is not None:
            entity_labels = list(set([e["label"] for e in self.entities if e["label"] in focus_entity]))
        else:
            entity_labels = list(set([e["label"] for e in self.entities]))
        color_map = {e: colors[i] for i, e in enumerate(entity_labels)}

        print("COLOR-ENTITY KEY: ")
        for entity, color in color_map.items():
            print(color + entity + '\033[0m')
        print("\n\n")

        annotated_text = ''
        track_idx = 0
        for i, e in enumerate(sorted(self.entities, key=lambda d: d["start_idx"])):
            cmap = color_map[e["label"]]

            annotated_text += self.raw_text[track_idx:e["start_idx"]]

            annotated_text += cmap + self.raw_text[e["start_idx"]:e["end_idx"]] + '\033[0m'

            track_idx = e["end_idx"]

            if i == len(self.entities) - 1:
                annotated_text += self.raw_text[e["end_idx"]:]

        print(annotated_text)

    def save(self, save_path):
        """
        Saves the annotated object to the specified location where the object will be saved where the final location is
        the base_path provided and the unique obj_id.
        :return:
        """
        if Path(save_path).exists():
            overwrite = input("File already exists.  Would you like to overwrite existing file? (y/n)")

            if overwrite.lower() == "y":
                json.dump(self.__dict__, open(save_path, "w"))
        else:
            json.dump(self.__dict__, open(save_path, "w"))
