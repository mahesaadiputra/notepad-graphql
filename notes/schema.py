from dataclasses import fields
from email import message
from pyexpat import model
from sre_constants import SUCCESS
from turtle import update
import graphene
from graphene_django import DjangoObjectType,DjangoListField
from .models import Notes
from users.models import ExtendUser
from users.schema import AuthMutation
from graphql_jwt.decorators import login_required

class UserNote(DjangoObjectType):
    class Meta:
        model = Notes
        fields = ("id","user","note","created_at","updated_at")
        
class UserData(DjangoObjectType):
    class Meta:
        model = ExtendUser
        fields = ("id","username","email")

class Query(AuthMutation,graphene.ObjectType):
    all_notes = graphene.List(UserNote)
    
    
    @login_required
    def resolve_all_notes(root,info):
        return Notes.objects.filter(user=info.context.user.id)
    
    
class CreateNotes(graphene.Mutation):
    
    class Arguments:
        note_text = graphene.String(required=True)

    success = graphene.Boolean()
    new_note = graphene.String()
     
    @login_required 
    def mutate(cls,info,note_text):
        note = Notes(note=note_text,user=info.context.user)
        note.save()
        return CreateNotes(success=True,
                           new_note =  note.note
                           )
    
    
class UpdateNotes(graphene.Mutation):
    
    class Arguments:
        id = graphene.ID(required=True)
        note_text = graphene.String(required=True)

    old_note = graphene.String()
    new_note = graphene.String()
    success = graphene.Boolean()
     
    @login_required   
    def mutate(cls,info,note_text,id):
        note = Notes.objects.get(id=id,user=info.context.user.id)
        old_note = note.note
        note.note = note_text
        note.save()
        return UpdateNotes(success=True,old_note=old_note,new_note=note_text)
    
class DeleteNotes(graphene.Mutation):
    
    class Arguments:
        id = graphene.ID(required=True)
        
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(cls,info,id):
        note = Notes.objects.get(id=id,user=info.context.user.id)
        note.delete()
        return DeleteNotes(success=True,message="Note deleted")
    
class Mutation(AuthMutation,graphene.ObjectType):
    create_note = CreateNotes.Field()
    update_note = UpdateNotes.Field()
    delete_note = DeleteNotes.Field()
    
    
    
schema = graphene.Schema(query=Query,mutation=Mutation)