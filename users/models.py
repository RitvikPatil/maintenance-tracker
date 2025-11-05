import logging
from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Create and save a user with the given email, first name, last name, and password.
        
        Args:
            email (str): User's email address (must be unique)
            first_name (str): User's first name
            last_name (str): User's last name
            password (str, optional): User's password. Defaults to None.
            
        Returns:
            User: The created user instance
            
        Raises:
            ValueError: If email is not provided
        """
        if not email:
            logger.error("User creation failed: Email is required")
            raise ValueError("Users must have an email address")
            
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        logger.info(f"User created successfully: {user.email}")
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Create and save a superuser with the given email, first name, last name, and password.
        
        Args:
            email (str): Superuser's email address
            first_name (str): Superuser's first name
            last_name (str): Superuser's last name
            password (str, optional): Superuser's password. Defaults to None.
            
        Returns:
            User: The created superuser instance
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            logger.warning("Superuser must have is_staff=True")
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            logger.warning("Superuser must have is_superuser=True")
            raise ValueError('Superuser must have is_superuser=True.')

        logger.info(f"Creating superuser: {email}")
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom user model that uses email as the unique identifier instead of username.
    Inherits from AbstractBaseUser for basic user functionality and BaseModel for common fields.
    """
    
    email = models.EmailField(
        unique=True,
        verbose_name="email address",
        help_text="User's unique email address"
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name="first name",
        help_text="User's first name"
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="last name",
        help_text="User's last name"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="active",
        help_text="Designates whether this user should be treated as active"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="staff status",
        help_text="Designates whether the user can log into this admin site"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date joined",
        help_text="Date when the user account was created"
    )

    # Custom user model configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        """Return string representation of the user (email)."""
        return self.email
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        
        Returns:
            str: User's full name
        """
        full_name = f"{self.first_name} {self.last_name}"
        logger.debug(f"Retrieved full name for user {self.email}: {full_name}")
        return full_name.strip()
    
    def get_short_name(self):
        """
        Return the short name for the user (first name).
        
        Returns:
            str: User's first name
        """
        logger.debug(f"Retrieved short name for user {self.email}: {self.first_name}")
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        
        Args:
            subject (str): Email subject
            message (str): Email message content
            from_email (str, optional): Sender's email address. Defaults to None.
        """
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email], **kwargs)
        logger.info(f"Email sent to {self.email} with subject: {subject}")

    def save(self, *args, **kwargs):
        """Override save method to add custom logic before saving."""
        # Add any pre-save logic here
        if not self.pk:
            logger.info(f"Creating new user: {self.email}")
        super().save(*args, **kwargs)
        logger.debug(f"User {self.email} saved successfully")